"""
The module containing the dataclass representing Python subroutine parameters.
"""

from __future__ import annotations
from dataclasses import dataclass
from inspect import Parameter as PythonParameter
from typing import Callable
from .serialized import Serialized
from .structure import Structure


@dataclass(frozen=True, slots=True)
class Parameter(Structure):
    """
    The dataclass representing Python subroutine parameters.
    """
    name: str
    description: str
    annotation: str
    default: str | None
    is_optional: bool

    @classmethod
    def from_parameter(cls, parameter: PythonParameter, docstring_parameters: list[Parameter]) -> Parameter:
        """
        Forms an instance of this class from a Python parameter, as provided by the in-built inspect API.
        
        :param parameter: The inspected parameter
        :param docstring_parameters: A list of parameters specified in the corresponding subroutine docstring
        :return: A corresponding instance of this class
        """
        try:
            docstring_parameter = next(filter(
                lambda docstring_parameter_: parameter.name == docstring_parameter_.name, docstring_parameters
            ))
            description = docstring_parameter.description
        except StopIteration:
            description = None
        return cls(
            parameter.name,
            description,
            cls.object_as_written(parameter.annotation),
            cls.object_as_written(parameter.default),
            not (parameter.kind in (
                PythonParameter.POSITIONAL_ONLY, PythonParameter.POSITIONAL_OR_KEYWORD
            ) and parameter.default == PythonParameter.empty)
        )

    def serialize(self, child_filter: Callable[[Structure], bool] = lambda _: True) -> Serialized:
        return Serialized(
            "Parameter",
            {
                "name": self.name,
                "description": self.description,
                "annotation": self.annotation,
                "default": self.default,
                "isOptional": self.is_optional
            },
            {}
        )
