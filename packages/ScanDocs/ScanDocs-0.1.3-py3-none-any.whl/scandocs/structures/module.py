"""
The module containing the dataclass representing Python modules (.py files).
"""

from __future__ import annotations
from dataclasses import dataclass
from inspect import getmembers, isclass, isfunction
from types import ModuleType, FunctionType
from typing import Callable
from .docstring import Docstring
from .structure import Structure
from .class_ import Class
from .serialized import Serialized
from .source_structure import SourceStructure
from .subroutine import Subroutine
from .searchable_structure import SearchableStructure
from .variable import Variable
from ..tags import Deprecated, Example, Link, Note


@dataclass(frozen=True, slots=True)
class Module(SourceStructure[ModuleType], SearchableStructure):
    """
    The dataclass representing Python modules (.py files).
    """
    classes: list[Class]
    subroutines: list[Subroutine]
    global_variables: list[Variable]

    @property
    def search_terms(self) -> str:
        return (
            f"{self.name}\n{self.docstring.short_description if self.docstring else ''}"
            f"\n{self.docstring.long_description if self.docstring else ''}"
        )

    @property
    def search_category(self) -> str:
        return "module"

    @classmethod
    def from_module(cls, module: ModuleType, declared: set[type | FunctionType]) -> Module:
        """
        Forms an instance of this class from an imported module.

        :param module: The module to form an object from
        :param declared: A set of structures that have already been declared before this module was loaded
        :return: A corresponding instance of this class
        """
        name = module.__name__.split(".")[-1]
        docstring = cls.get_docstring(module)
        return cls(
            name,
            cls.check_is_private(module),
            name.startswith("__"),
            cls.get_source(module),
            Docstring.from_docstring(docstring) if docstring else None,
            Deprecated.get_tags(module),
            Example.get_tags(module),
            Link.get_tags(module),
            Note.get_tags(module),
            [Class.from_class(class_[1], class_[1] in declared)
             for class_ in getmembers(
                module, predicate=lambda member: isclass(member) and cls.defined_within(member, module.__name__)
            )],
            [Subroutine.from_subroutine(subroutine[1], subroutine[1] in declared)
             for subroutine in getmembers(
                module, predicate=lambda member: isfunction(member) and cls.defined_within(member, module.__name__)
            )],
            [variable for variable in Variable.many_from_scope(
                module, module.__name__, lambda variable: not callable(variable)
            )]
        )

    def serialize(self, child_filter: Callable[[Structure], bool] = lambda _: True) -> Serialized:
        return Serialized(
            "Module",
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
                "searchTerms": self.search_terms,
                "globalVariables": [
                    variable.serialize(
                        child_filter=child_filter).to_json()
                    for variable in self.global_variables if child_filter(variable)
                ]
            },
            {
                "Classes": [
                    class_.serialize(child_filter=child_filter) for class_ in self.classes
                ],
                "Subroutines": [
                    subroutine.serialize(
                        child_filter=child_filter) for subroutine in self.subroutines if child_filter(subroutine)
                ]
            }
        )
