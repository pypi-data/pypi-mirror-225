"""
Server for OctoAI endpoints created with the ``octoai`` CLI.

Developers that want to create an endpoint should not use
this module directly. Instead, they should use the ``octoai``
command-line interface, which directs them to implement the
``octoai.service.Service`` class and use the ``octoai`` CLI to help
build and deploy their endpoint.
"""
import asyncio
import importlib
import inspect
import json
import multiprocessing
import os
import signal
import sys
import time
from contextlib import asynccontextmanager
from http import HTTPStatus
from multiprocessing import Pipe
from multiprocessing.connection import Connection
from typing import Any, Dict, NamedTuple, Optional

import click
import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from .service import (
    ResponseAnalytics,
    Service,
    inspect_input_types,
    inspect_output_types,
)

_OCTOAI_SERVICE_MODULE = "octoai.service"
_OCTOAI_BASE_SERVICE_CLASS = "Service"


_PREDICT_LOOP_WATCHDOG_SECONDS = 2
"""Delay in seconds between checking if the predict loop is running."""


_process_mutex = multiprocessing.Lock()
"""Lock for spawning predict loop."""


class InferenceRequest(NamedTuple):
    """Class for returning inference results."""

    response_pipe: Connection
    inputs: Any


class InferenceResponse(NamedTuple):
    """Class for returning inference results."""

    inference_time_ms: float
    outputs: Any


def _predict_loop(service, _request_queue):
    """Loop which handles prediction requests.

    This loop runs for the duration of the server and receives prediction
    requests posted to the _REQUEST_QUEUE. When the request is done processing
    the results are posted to the response_pipe where they are handled by
    the main /predict endpoint.
    """
    service.setup()

    def signal_handler(_signum, _frame):
        # This will only kill the _predict_loop process, not the parent
        sys.exit()

    signal.signal(signal.SIGINT, signal_handler)

    while True:
        try:
            inference_request = _request_queue.get()
            try:
                start_time = time.perf_counter_ns()
                results = service.infer(**inference_request.inputs)
                stop_time = time.perf_counter_ns()
                response = InferenceResponse((stop_time - start_time) / 1e9, results)
            except Exception as e:
                response = e
            inference_request.response_pipe.send(response)
        except Exception:
            # We only end up here if something went wrong outside the predict call
            # continue loop
            pass


class Server:
    """
    Server for OctoAI endpoints created with the ``octoai`` CLI.

    Developers that want to create an endpoint should not use
    this class directly. Instead, they should use the ``octoai``
    command-line interface, which directs them to implement the
    ``octoai.service.Service`` class and use the ``octoai`` CLI to
    help build and deploy their endpoint.
    """

    def __init__(self, service: Service, async_enable: bool = True):
        @asynccontextmanager
        async def _lifespan(app: FastAPI):
            _predict_loop_watchdog_task = asyncio.create_task(
                self._predict_loop_watchdog(  # noqa
                    _PREDICT_LOOP_WATCHDOG_SECONDS, self._check_predict_loop  # noqa
                )
            )
            yield
            _predict_loop_watchdog_task.cancel()

        lifespan = _lifespan if async_enable else None

        self.app = FastAPI(lifespan=lifespan)
        self.service = service
        self.status = HTTPStatus.SERVICE_UNAVAILABLE
        self.is_async = async_enable
        self._request_queue: multiprocessing.Queue[Any] = None

        self.response_headers = {
            "OCTOAI_REPLICA_NAME": os.environ.get("OCTOAI_REPLICA_NAME", ""),
        }

        Input = inspect_input_types(service)
        Output = inspect_output_types(service)

        @self.app.get("/healthcheck")
        def health() -> JSONResponse:
            if self.is_async and not self._predict_process.is_alive():
                self.status = HTTPStatus.SERVICE_UNAVAILABLE
            return JSONResponse(
                status_code=self.status.value, content={"status": self.status.name}
            )

        @self.app.get("/")
        def root() -> JSONResponse:
            return JSONResponse(
                status_code=HTTPStatus.OK,
                content={
                    "docs": "/docs",
                    "openapi": "/openapi.json",
                },
            )

        @self.app.post(
            "/infer",
            response_model=Output,
        )
        async def infer(request: Input):
            infer_args = {k: v for k, v in request}

            async def _pipe_reader(read):
                """Async multiprocessing.Pipe reader.

                :param read: pipe file handle to read from.
                :return: the contents of the pipe when read.
                """
                data_available = asyncio.Event()
                asyncio.get_event_loop().add_reader(read.fileno(), data_available.set)
                if not read.poll():
                    await data_available.wait()
                result = read.recv()
                data_available.clear()
                asyncio.get_event_loop().remove_reader(read.fileno())
                return result

            if self.is_async:
                read_conn, write_conn = Pipe()
                start_perf = time.perf_counter_ns()
                self._request_queue.put(InferenceRequest(write_conn, infer_args))
                response = await _pipe_reader(read_conn)
                performance_time_ms = (time.perf_counter_ns() - start_perf) / 1e6
                if isinstance(response, Exception):
                    raise response

                prediction = response.outputs
                inference_time_ms = response.inference_time_ms
            else:
                # track time elapsed in nanoseconds only while app is not asleep
                start_process = time.process_time_ns()
                # track time elapsed in nanoseconds including any sleep time
                start_perf = time.perf_counter_ns()
                prediction = service.infer(**infer_args)
                inference_time_ms = (time.process_time_ns() - start_process) / 1e6
                performance_time_ms = (time.perf_counter_ns() - start_perf) / 1e6
            return JSONResponse(
                status_code=HTTPStatus.OK,
                headers=self.response_headers,
                content=Output(
                    output=prediction,
                    analytics=ResponseAnalytics(
                        inference_time_ms=inference_time_ms,
                        performance_time_ms=performance_time_ms,
                    ),
                ).model_dump(),
            )

    async def _check_predict_loop(self):
        if not self._predict_process.is_alive():
            self._start_predict_loop()

    def _start_predict_loop(self):
        with _process_mutex:
            context = multiprocessing.get_context("spawn")
            if not self._request_queue:
                # Only need to create this queue once. This function may be called
                # multiple times if the predict loop dies.
                self._request_queue = context.Queue()

            self._predict_process = context.Process(
                target=_predict_loop,
                name="_predict_loop",
                args=(self.service, self._request_queue),
            )
            self._predict_process.start()

    async def _predict_loop_watchdog(self, interval, periodic_function):
        while True:
            await asyncio.gather(
                asyncio.sleep(interval),
                periodic_function(),
            )

    def get_api_schema(self) -> Dict[str, Any]:
        """Return the Open API schema for the underlying service."""
        return self.app.openapi()

    def init(self):
        """Initialize the underlying service."""
        try:
            if self.is_async:
                # load_into_memory is handled in predict loop so that subprocess
                # does all GPU access.
                self._start_predict_loop()
            else:
                self.service.setup()

            self.status = HTTPStatus.OK
        except Exception as e:
            self.status = HTTPStatus.SERVICE_UNAVAILABLE
            raise e

    def run(self, port: int, timeout_keep_alive: int):
        """Run the server exposing the underlying service."""
        uvicorn.run(
            self.app,
            host="0.0.0.0",
            port=port,
            timeout_keep_alive=timeout_keep_alive,
            lifespan="on",
        )


def load_service(module_name: str, class_name: Optional[str]) -> Service:
    """Load the service implementation."""
    try:
        module = importlib.import_module(module_name)

        if class_name is not None:
            # if service class is provided, instantiate it
            class_ = getattr(module, class_name)
        else:
            # if service class not provided, look for it
            class_ = None
            for name, class_obj in inspect.getmembers(module, inspect.isclass):
                for class_base in class_obj.__bases__:
                    if (
                        class_base.__module__ == _OCTOAI_SERVICE_MODULE
                        and class_base.__name__ == _OCTOAI_BASE_SERVICE_CLASS
                    ):
                        class_ = class_obj
                        break

            if class_ is None:
                raise ValueError(
                    f"Module '{module_name}' contains no classes extending "
                    f"base '{_OCTOAI_SERVICE_MODULE}.{_OCTOAI_BASE_SERVICE_CLASS}'"
                )

        click.echo(f"Using service in {module_name}.{class_.__name__}.")

        return class_()
    except ModuleNotFoundError:
        error_msg = f"Module '{module_name}' not found. "
        if module_name == "service":
            error_msg += "Ensure your service is defined in service.py."
        raise ValueError(error_msg)


@click.group(name="server")
@click.option("--service-module", default="service")
@click.option("--service-class", default=None)
@click.option("--async-enable", default=True)
@click.pass_context
def server(ctx, service_module, service_class, async_enable):
    """CLI for OctoAI server."""
    click.echo("octoai server")
    ctx.ensure_object(dict)
    service = load_service(service_module, service_class)
    ctx.obj["server"] = Server(service, async_enable=async_enable)


@server.command()
@click.option("--output-file", default=None)
@click.pass_context
def api_schema(ctx, output_file):
    """Generate OpenAPI schema for the given service."""
    click.echo("api-schema")
    server = ctx.obj["server"]
    schema = server.get_api_schema()

    if output_file:
        with open(output_file, "w") as f:
            json.dump(schema, f, indent=2)
    else:
        click.echo(json.dumps(schema, indent=2))


@server.command()
@click.pass_context
def setup_service(ctx):
    """Run the setup code for the given service."""
    click.echo("setup-service")
    server = ctx.obj["server"]
    server.init()


@server.command()
@click.pass_context
@click.option("--port", type=int, default=8080)
@click.option(
    "--timeout-keep-alive",
    type=int,
    default=900,
    help="Connection keep alive timeout in seconds",
)
def run(ctx, port, timeout_keep_alive):
    """Run the server for the given service."""
    click.echo("run")
    server = ctx.obj["server"]
    server.init()
    server.run(port, timeout_keep_alive)


if __name__ == "__main__":
    server(obj={})
