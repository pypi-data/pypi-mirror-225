"""
The module containing the dataclass representing Python subroutines, such as functions, methods, and generators.
"""

from __future__ import annotations
from dataclasses import dataclass
from types import FunctionType
from typing import Callable
from inspect import isgeneratorfunction, isasyncgenfunction, iscoroutinefunction
from .docstring import Docstring
from .structure import Structure
from .signature_structure import SignatureStructure
from .serialized import Serialized
from .parameter import Parameter
from .subroutine_return import SubroutineReturn
from .searchable_structure import SearchableStructure
from ..tags import ContextManager, Deprecated, Link, Note, Example


@dataclass(frozen=True, slots=True)
class Subroutine(SignatureStructure[FunctionType], SearchableStructure):
    """
    The dataclass representing Python subroutines, such as functions, methods, and generators.
    """
    @property
    def search_terms(self) -> str:
        return (
            f"{self.name}\n{self.docstring.short_description if self.docstring else ''}"
            f"\n{self.docstring.long_description if self.docstring else ''}"
        )

    @property
    def search_category(self) -> str:
        return "subroutine"

    parameters: list[Parameter]
    is_generator: bool | None
    is_async: bool
    is_abstract: bool
    is_lambda: bool
    is_context_manager: bool

    @classmethod
    def from_subroutine(cls, subroutine: FunctionType | type(object.__init__), is_declared: bool,
                        is_abstract: bool = False) -> Subroutine:
        """
        Forms an instance of this class from a Python subroutine, as provided by the in-built inspect API.
        
        :param subroutine: The inspected subroutine
        :param is_declared: Whether the subroutine has been previously declared or not
        :param is_abstract: Whether this subroutine is an abstract method or not
        :return: A corresponding instance of this class
        """
        name = subroutine.__name__
        signature = cls.get_signature(subroutine)
        docstring = cls.get_docstring(subroutine)
        docstring = Docstring.from_docstring(
            docstring, cls.object_as_written(signature.return_annotation)
        ) if docstring else None

        return cls(
            name,
            cls.check_is_private(subroutine),
            name.startswith("__"),
            cls.get_source(subroutine),
            docstring,
            Deprecated.get_tags(subroutine),
            Example.get_tags(subroutine),
            Link.get_tags(subroutine),
            Note.get_tags(subroutine),
            is_declared,
            signature,
            [
                Parameter.from_parameter(
                    signature.parameters[parameter], docstring.parameters if docstring else []
                ) for parameter in signature.parameters if parameter is not None
            ],
            isgeneratorfunction(subroutine) or isasyncgenfunction(subroutine),
            (
                isasyncgenfunction(subroutine) or
                iscoroutinefunction(subroutine) or
                (
                    any(tag.is_async for tag in ContextManager.get_tags(subroutine))
                    if ContextManager.is_tagged(subroutine) else False
                )
            ),
            is_abstract,
            name == "<lambda>",
            ContextManager.is_tagged(subroutine)
        )

    def serialize(self, child_filter: Callable[[Structure], bool] = lambda _: True) -> Serialized:
        return Serialized(
            "Subroutine",
            {
                "searchCategory": self.search_category,
                "name": self.name,
                "source": self.source,
                "signature": str(self.signature),
                "parameters": [
                    parameter.serialize(child_filter=child_filter).to_json() for parameter in self.parameters
                ],
                "raises": [
                    error.serialize(child_filter=child_filter).to_json() for error in self.docstring.raises
                ] if self.docstring else [],
                "returns": [
                    return_.serialize(child_filter=child_filter).to_json() for return_ in self.docstring.returns
                ] if self.docstring else [
                    SubroutineReturn(
                        "No description...", self.object_as_written(self.signature.return_annotation)
                    ).serialize(child_filter=child_filter).to_json()
                ],
                "shortDescription": self.docstring.short_description if self.docstring else None,
                "longDescription": self.docstring.long_description if self.docstring else None,
                "deprecations": [deprecation.json_serialize() for deprecation in self.deprecations],
                "examples": [example.json_serialize() for example in self.examples],
                "links": [link.json_serialize() for link in self.links],
                "notes": [note.json_serialize() for note in self.notes],
                "isGenerator": self.is_generator,
                "isAsync": self.is_async,
                "isAbstract": self.is_abstract,
                "isLambda": self.is_lambda,
                "isContextManager": self.is_context_manager,
                "searchTerms": self.search_terms
            },
            {}
        )
