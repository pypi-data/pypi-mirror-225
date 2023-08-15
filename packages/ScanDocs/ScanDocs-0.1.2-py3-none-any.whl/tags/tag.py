"""
A module containing internal details of how the tag API is structured.

This module contains an abstract base class, which dictates how each tag
must be interfaced with, and how they relay their information to the parser
to be placed in the generated documentation website.
"""

from __future__ import annotations
from dataclasses import dataclass
from types import ModuleType
from typing import Callable, TypeVar
from abc import ABC
from sys import modules


@dataclass(frozen=True, slots=True)
class Tag(ABC):
    """
    An ABC dictating how the tag API must be structured.

    This dataclass provides a template for all public tags in the API,
    ensuring that they are all interfaced with in the same way.
    """
    @staticmethod
    def get_all_tags(f: Callable | ModuleType) -> dict[str, list[Tag]]:
        """
        Retrieves all the tags from a given structure, irrespective of type.

        :param f: The given structure to retrieve from
        :return: A mapping of tag names to a list of corresponding tags
        """
        try:
            # noinspection PyUnresolvedReferences
            return f.__scandocs_tags__
        except AttributeError:
            return {}

    @classmethod
    def get_tags(cls: OwnTagT, f: Callable | ModuleType) -> list[OwnTagT]:
        """
        Gets the tag of the specified type from a given structure.

        Retrieves the first tag corresponding to the specified tag type from
        the given structure, should it exist.

        :param f: The given structure to retrieve from
        :return: If a tag exists of the correct type, return it
        """
        return cls.get_all_tags(f).get(cls.__name__, [])

    def tag(self, f: Callable | ModuleType) -> Callable | ModuleType:
        """
        Tags a structure with a reference to the specified tag.

        This method can be used as a decorator to tag structures as desired
        with a concise and readable syntax.

        :param f: The structure to tag
        :return: The given structure, with the given tag attached

        """
        if hasattr(f, "__scandocs_tags__"):
            if self.__class__.__name__ in f.__scandocs_tags__:
                f.__scandocs_tags__[self.__class__.__name__].append(self)
            else:
                f.__scandocs_tags__[self.__class__.__name__] = [self]
        else:
            f.__scandocs_tags__ = {self.__class__.__name__: [self]}
        return f

    def __call__(self, f: Callable | ModuleType) -> Callable | ModuleType:
        """
        Tags a structure with a reference to the specified tag.

        This has the same functionality as calling the tag method, and serves only to simplify the API.

        :param f: The structure to tag
        :return: The given structure, with an attached tag
        """
        return self.tag(f)

    @classmethod
    def is_tagged(cls, f: Callable | ModuleType) -> bool:
        """
        A utility method to check if any tags of this type exist on a structure.

        :param f: The structure which may have tags attached to it
        :return: Whether the given structure has any tags of the correct type
        """
        return any(isinstance(tag, cls) for tag_list in cls.get_all_tags(f).values() for tag in tag_list)

    @staticmethod
    def module_from_name(module_name: str) -> ModuleType | None:
        return modules.get(module_name)


OwnTagT = TypeVar("OwnTagT", bound=Tag)
