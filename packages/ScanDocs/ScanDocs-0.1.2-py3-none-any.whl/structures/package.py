"""
The module containing the dataclass representing Python packages (__init__.py files in a project folder).
"""

from __future__ import annotations
from dataclasses import dataclass
from types import ModuleType, FunctionType
from inspect import getmembers, ismodule, isclass, isfunction
from typing import Callable
from .docstring import Docstring
from .structure import Structure
from .module import Module
from .serialized import Serialized
from .source_structure import SourceStructure
from .searchable_structure import SearchableStructure
from ..tags import Deprecated, Example, Link, Note


@dataclass(frozen=True)
class Package(SourceStructure[ModuleType], SearchableStructure):
    """
    The dataclass representing Python packages (__init__.py files in a project folder).
    """
    subpackages: list[Package]
    modules: list[Module]

    @property
    def search_terms(self) -> str:
        return (
            f"{self.name}\n{self.docstring.short_description if self.docstring else ''}"
            f"\n{self.docstring.long_description if self.docstring else ''}"
        )

    @property
    def search_category(self) -> str:
        return "package"

    @classmethod
    def from_module(cls, package: ModuleType, declared: set[type | FunctionType] | None = None) -> Package:
        """
        Forms an instance of this class from an imported package.

        Initially checks __all__ for any submodules / subpackages that may be missed,
        before adding all those publicly available via the in-built inspect API to the list of substructures.

        :param package: The package to form an object from
        :param declared: A set of structures that have already been declared before this module was loaded
        :return: A corresponding instance of this class
        """
        if not cls.is_package(package):
            raise TypeError("Can't build documentation for non-package") from None

        if declared is None:
            declared = cls.get_declared(package)
        else:
            declared = declared.intersection(cls.get_declared(package))

        name = package.__name__.split(".")[-1]
        docstring = cls.get_docstring(package)
        try:
            substructures = [substructure for substructure in package.__all__ if ismodule(substructure)]
        except AttributeError:  # __all__ index not defined
            substructures = []
        substructures += [substructure[1] for substructure in getmembers(package, predicate=ismodule)]

        return cls(
            name,
            cls.check_is_private(package),
            name.startswith("__"),
            cls.get_source(package),
            Docstring.from_docstring(docstring) if docstring else None,
            Deprecated.get_tags(package),
            Example.get_tags(package),
            Link.get_tags(package),
            Note.get_tags(package),
            [cls.from_module(structure, declared) for structure in substructures if cls.is_package(structure)],
            [Module.from_module(structure, declared) for structure in substructures if not cls.is_package(structure)]
        )

    @staticmethod
    def is_package(package: ModuleType) -> bool:
        """
        Determines whether a given module is a package or a module (whether it is an __init__.py file or not).

        :param package: The module to inspect
        :return: Whether the given module is a package (__init__.py file) or not
        """
        return package.__package__ == package.__name__

    @staticmethod
    def get_declared(package: ModuleType) -> set[type | FunctionType]:
        """
        Gets the declared members (classes and subroutines) from a given package.

        :param package: The package to inspect
        :return: A set of the declared classes and subroutines
        """
        return set(member[1] for member in getmembers(
            package,
            predicate=lambda member: isclass(member) or isfunction(member)
        ))

    def serialize(self, child_filter: Callable[[Structure], bool] = lambda _: True) -> Serialized:
        return Serialized(
            "Package",
            {
                "searchCategory": self.search_category,
                "name": self.name,
                "source": self.source,
                "shortDescription": self.docstring.short_description if self.docstring else None,
                "longDescription": self.docstring.long_description if self.docstring else None,
                "deprecations": [deprecation.json_serialize() for deprecation in self.deprecations],
                "examples": [example.json_serialize() for example in self.examples],
                "links": [link.json_serialize() for link in self.links],
                "notes": [note.json_serialize() for note in self.notes],
                "searchTerms": self.search_terms
            },
            {
                "Sub-Packages": [
                    subpackage.serialize(
                        child_filter=child_filter) for subpackage in self.subpackages if child_filter(subpackage)
                ],
                "Modules": [
                    module.serialize(child_filter=child_filter) for module in self.modules if child_filter(module)
                ]
            }
        )
