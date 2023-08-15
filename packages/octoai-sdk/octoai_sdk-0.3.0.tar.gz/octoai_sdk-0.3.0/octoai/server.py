"""
Server for OctoAI endpoints created with the ``octoai`` CLI.

Developers that want to create an endpoint should not use
this module directly. Instead, they should use the ``octoai``
command-line interface, which directs them to implement the
``octoai.service.Service`` class and use the ``octoai`` CLI to help
build and deploy their endpoint.
"""
import importlib
import inspect
import json
import os
import time
from enum import Enum
from typing import Any, Dict, Optional

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


class HealthStatus(Enum):
    """HTTP status codes for health check."""

    STARTING = 503
    UNKNOWN = 500
    READY = 200


class Server:
    """
    Server for OctoAI endpoints created with the ``octoai`` CLI.

    Developers that want to create an endpoint should not use
    this class directly. Instead, they should use the ``octoai``
    command-line interface, which directs them to implement the
    ``octoai.service.Service`` class and use the ``octoai`` CLI to
    help build and deploy their endpoint.
    """

    def __init__(self, service: Service):
        self.app = FastAPI()
        self.service = service
        self.status = HealthStatus.STARTING

        self.response_headers = {
            "OCTOAI_REPLICA_NAME": os.environ.get("OCTOAI_REPLICA_NAME", ""),
        }

        Input = inspect_input_types(service)
        Output = inspect_output_types(service)

        @self.app.get("/healthcheck")
        def health() -> JSONResponse:
            return JSONResponse(
                status_code=self.status.value, content={"status": self.status.name}
            )

        @self.app.get("/")
        def root() -> JSONResponse:
            return JSONResponse(
                status_code=200,
                content={
                    "docs": "/docs",
                    "openapi": "/openapi.json",
                },
            )

        @self.app.post(
            "/infer",
            response_model=Output,
        )
        def infer(request: Input):
            infer_args = {k: v for k, v in request}

            # track time elapsed in nanoseconds only while app is not asleep
            start_process = time.process_time_ns()
            # track time elapsed in nanoseconds including any sleep time
            start_perf = time.perf_counter_ns()
            prediction = service.infer(**infer_args)
            inference_time_ms = (time.process_time_ns() - start_process) / 1e6
            performance_time_ms = (time.perf_counter_ns() - start_perf) / 1e6

            return JSONResponse(
                status_code=200,
                headers=self.response_headers,
                content=Output(
                    output=prediction,
                    analytics=ResponseAnalytics(
                        inference_time_ms=inference_time_ms,
                        performance_time_ms=performance_time_ms,
                    ),
                ).model_dump(),
            )

    def get_api_schema(self) -> Dict[str, Any]:
        """Return the Open API schema for the underlying service."""
        return self.app.openapi()

    def init(self):
        """Initialize the underlying service."""
        try:
            self.service.setup()
            self.status = HealthStatus.READY
        except Exception as e:
            self.status = HealthStatus.UNKNOWN
            raise e

    def run(self, port: int, timeout_keep_alive: int):
        """Run the server exposing the underlying service."""
        uvicorn.run(
            self.app,
            host="0.0.0.0",
            port=port,
            timeout_keep_alive=timeout_keep_alive,
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
@click.pass_context
def server(ctx, service_module, service_class):
    """CLI for OctoAI server."""
    click.echo("octoai server")
    ctx.ensure_object(dict)
    service = load_service(service_module, service_class)
    ctx.obj["server"] = Server(service)


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
