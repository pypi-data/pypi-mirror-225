"""
The module containing the dataclass representing any public variables, such as class variables.
"""

from __future__ import annotations
from dataclasses import dataclass
from types import ModuleType
from typing import Iterable, Callable
from inspect import Signature, getmembers
from .serialized import Serialized
from .structure import Structure


@dataclass(frozen=True, slots=True)
class Variable(Structure):
    """
    The dataclass representing any public variables, such as class variables.
    """
    name: str
    annotation: str | None
    value: str

    @classmethod
    def many_from_scope(cls, scope: object | ModuleType, module_name: str,
                        variable_filter: Callable[[object], bool] = lambda _: True) -> Iterable[Variable]:
        """
        Forms an instance of this class from a valid scope, such as a class or module.

        :param scope: The scope to retrieve variables from
        :param module_name: The name of the module in which the variable is located
        :param variable_filter: A filter function to narrow the selection of yielded variables
        :return: Each discovered variable from the given scope
        """
        def is_valid(variable: object) -> bool:
            return (
                cls.defined_within(variable, module_name) and variable_filter(variable)
                and not cls.check_is_private(variable)
            )

        variable_information = getmembers(scope)
        try:
            annotations_ = vars(scope).__annotations__
        except AttributeError:
            annotations_ = {}
        variables = {name: variable for name, variable in variable_information if is_valid(variable)}
        for variable_name in variables:
            yield cls(
                variable_name,
                cls.object_as_written(annotations_.get(variable_name, Signature.empty)),
                cls.object_as_written(variables.get(variable_name, Signature.empty))
            )

    def serialize(self, child_filter: Callable[[Structure], bool] = lambda _: True) -> Serialized:
        return Serialized(
            "Variable",
            {
                "name": self.name,
                "annotation": self.annotation,
                "value": self.value
            },
            {}
        )
