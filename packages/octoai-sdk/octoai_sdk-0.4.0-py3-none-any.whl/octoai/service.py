"""
Contains the base interface that OctoAI endpoints should implement.

Developers that want to create an endpoint should implement the
``Service`` class in this module as directed by the ``octoai`` command-line
interface.
"""
import inspect
from abc import ABC, abstractmethod
from collections import OrderedDict
from typing import Any, Type

from pydantic import BaseModel, Field, create_model


class Service(ABC):
    """
    The base interface that OctoAI endpoints should implement.

    Developers that want to create an endpoint should implement this
    class as directed by the ``octoai`` command-line interface.
    """

    def setup(self) -> None:
        """
        Perform service initialization.

        A common operation to include here is loading weights and making
        those available to the ``infer()`` method in a member variable.
        """
        pass

    @abstractmethod
    def infer(self, **kwargs: Any) -> Any:
        """Perform inference."""
        pass


class ResponseAnalytics(BaseModel):
    """Additional analytics metadata."""

    inference_time_ms: float = Field(
        description="Inference execution time (without pauses)"
    )
    performance_time_ms: float = Field(
        description="Inference execution time (including pauses)"
    )


def inspect_input_types(service: Service) -> Type[BaseModel]:
    """Create Pydantic input model from ``infer()`` signature."""
    args = OrderedDict()
    signature = inspect.signature(service.infer)

    if len(signature.parameters) < 1:
        raise ValueError("infer() requires at least one argument")

    for arg_name, arg in signature.parameters.items():
        if arg.annotation == inspect._empty:
            raise ValueError("infer() requires type annotations for args")

        default = None if arg.default == inspect._empty else arg.default
        args[arg_name] = (arg.annotation, default)

    return create_model(
        "Input",
        __config__=None,
        __base__=BaseModel,
        __module__=__name__,
        __validators__=None,
        **args,
    )


def inspect_output_types(service: Service) -> Type[BaseModel]:
    """Create Pydantic output model from ``infer()`` signature."""
    signature = inspect.signature(service.infer)

    if signature.return_annotation == inspect._empty:
        raise ValueError("infer() requires a return type annotation")

    rets = OrderedDict()
    rets["output"] = (signature.return_annotation, None)
    rets["analytics"] = (ResponseAnalytics, None)

    return create_model(
        "Output",
        __config__=None,
        __base__=BaseModel,
        __module__=__name__,
        __validators__=None,
        **rets,
    )
