"""
The module containing the dataclass representing any Python structure recorded by the scanning tool for documenting.
"""

from __future__ import annotations
from dataclasses import dataclass
from inspect import Signature, getmodule
from types import ModuleType, FunctionType
from typing import Callable
from abc import ABC, abstractmethod
from .serialized import Serialized
from ..tags import Private


@dataclass(frozen=True, slots=True)
class Structure(ABC):
    """
    The base dataclass representing any Python structure recorded by the scanning tool for documenting.
    """

    @abstractmethod
    def serialize(self, child_filter: Callable[[Structure], bool] = lambda _: True) -> Serialized:
        """
        Serializes the structure into a Serialized object, so that it can be used in the website.

        A Serialized object is a standardized format for serialization structures, with customizable filtering
        options to omit certain structures from the project tree as desired,
        and a convenient method for conversion to JSON.

        :param child_filter: The filter method used to omit unwanted structures from the serializes project tree
        :return: The serialized structure, in a compatible JSON format
        """
        ...

    @staticmethod
    def object_as_written(object_: object) -> str | None:
        """
        Writes a given object in a more easily readable format.
         
        Writes a given object as it is expected to have been written in the source code.
        
        :param object_: The object as expected to have been written in source code
        :rtype: str
        :return: If the object has an empty signature, as per the in-built inspect API
        :rtype: None
        """
        if object_ in (Signature.empty, "_empty"):
            return
        return object_.__name__ if isinstance(object_, type) else str(object_)

    @staticmethod
    def defined_within(member, module_name: str) -> bool | None:
        """
        Determines whether a given member is in-built or not within a given module.

        :param member: The member to inspect
        :param module_name: the name of the module the member was declared within
        :return: Whether the member was defined in the given module, or imported / in-built
        :rtype: bool
        :return: If the source module of the given member cannot be determined
        :rtype: None
        """
        defined_module = getmodule(member)
        if defined_module is None:
            return
        return getmodule(member).__name__ == module_name

    @staticmethod
    def check_is_private(structure: object | FunctionType | ModuleType) -> bool:
        """
        Checks to see whether a structure is considered to be private.

        If a structure does not possess the private tag, and starts with
        at least one underscore, it is considered to be private.

        :param structure:
        :return:
        """
        if hasattr(structure, "__name__"):
            return Private.is_tagged(structure) or structure.__name__.startswith("_")
        return Private.is_tagged(structure)
