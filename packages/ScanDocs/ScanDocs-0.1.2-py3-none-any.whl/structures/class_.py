"""
The module containing the dataclass representing Python classes.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Callable
from inspect import isabstract, isdatadescriptor, ismemberdescriptor, ismethoddescriptor, isgetsetdescriptor
from .docstring import Docstring
from .structure import Structure
from .signature_structure import SignatureStructure
from .serialized import Serialized
from .subroutine import Subroutine
from .searchable_structure import SearchableStructure
from .variable import Variable
from ..tags import Deprecated, Link, Note, Example


@dataclass(frozen=True, slots=True)
class Class(SignatureStructure[type], SearchableStructure):
    """
    The dataclass representing Python classes.
    """
    methods: list[Subroutine]
    is_abstract: bool
    class_variables: list[Variable]

    @property
    def search_terms(self) -> str:
        return (
            f"{self.name}\n{self.docstring.short_description if self.docstring else ''}"
            f"\n{self.docstring.long_description if self.docstring else ''}"
        )

    @property
    def search_category(self) -> str:
        return "class"

    @classmethod
    def from_class(cls, class_: type, is_declared: bool) -> Class:
        name = class_.__name__
        docstring = cls.get_docstring(class_)
        try:
            abstract_methods = class_.__abstractmethods__
        except AttributeError:
            abstract_methods = []
        return cls(
            name,
            cls.check_is_private(class_),
            name.startswith("__"),
            cls.get_source(class_),
            Docstring.from_docstring(docstring) if docstring else None,
            Deprecated.get_tags(class_),
            Example.get_tags(class_),
            Link.get_tags(class_),
            Note.get_tags(class_),
            is_declared,
            cls.get_signature(class_),
            [
                Subroutine.from_subroutine(
                    getattr(class_, method),
                    is_declared,
                    is_abstract=method in abstract_methods
                )
                for method in class_.__dict__ if callable(getattr(class_, method))
            ],
            isabstract(class_),
            [
                variable for variable in Variable.many_from_scope(
                    class_, class_.__module__,
                    lambda variable: not (
                        ismemberdescriptor(variable) or isdatadescriptor(variable) or
                        ismethoddescriptor(variable) or isgetsetdescriptor(variable) or callable(variable)
                    )
                )
            ]
        )

    @property
    def initializer(self) -> Subroutine:
        return next(filter(
            lambda method: method.name == "__init__", self.methods), Subroutine.from_subroutine(object.__init__, False)
        )

    def serialize(self, child_filter: Callable[[Structure], bool] = lambda _: True) -> Serialized:
        return Serialized(
            "Class",
            {
                "searchCategory": self.search_category,
                "name": self.name,
                "source": self.source,
                "signature": str(self.signature),
                "parameters": self.initializer.serialize(child_filter=child_filter).meta.get("parameters", []),
                "shortDescription": self.docstring.short_description if self.docstring else None,
                "longDescription": self.docstring.long_description if self.docstring else None,
                "deprecations": [deprecation.json_serialize() for deprecation in self.deprecations],
                "examples": [example.json_serialize() for example in self.examples],
                "links": [link.json_serialize() for link in self.links],
                "notes": [note.json_serialize() for note in self.notes],
                "isAbstract": self.is_abstract,
                "searchTerms": self.search_terms,
                "classVariables": [
                    variable.serialize(child_filter=child_filter).to_json()
                    for variable in self.class_variables if child_filter(variable)
                ]
            },
            {
                "Methods": [
                    method.serialize(child_filter=child_filter) for method in self.methods if child_filter(method)
                ]
            }
        )
