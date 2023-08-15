"""
The module containing the dataclass representing any structure that has source code that can be inspected.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Generic, TypeVar
from inspect import getsource, getdoc
from docstring_parser import parse, Docstring as ParserDocstring
from abc import ABC
from .docstring import Docstring
from .structure import Structure
from ..tags import Deprecated, Example, Link, Note

StructureT = TypeVar("StructureT")


@dataclass(frozen=True, slots=True)
class SourceStructure(Generic[StructureT], Structure, ABC):
    """
    A structure that has source code that can be inspected by the in-built inspect API.
    """
    name: str
    is_private: bool
    is_dunder: bool
    source: str
    docstring: Docstring | None
    deprecations: list[Deprecated]
    examples: list[Example] | None
    links: list[Link] | None
    notes: list[Note] | None

    @staticmethod
    def get_source(structure: StructureT) -> str | None:
        """
        Gets the source code from a given structure.

        :param structure: The given structure to get the source code from
        :return: The source code of the given structure
        :rtype: str
        :return: If the source code cannot be provided
        :rtype: None
        """
        try:
            return getsource(structure)
        except OSError:
            return  # Can't be provided
        except TypeError:
            return  # Can't be provided, maybe builtin?

    @staticmethod
    def get_docstring(structure: StructureT) -> ParserDocstring | None:
        """
        Gets the docstring from a given structure.

        Uses the in-built inspect API to fetch the corresponding docstring from the structure,
        falling back to superclasses if necessary, and cleaning / sanitizing the docstring as required.

        :param structure: The structure to get a docstring from
        :rtype: docstring_parser.Docstring
        :return: If no docstring exists, or it consists of only empty space
        :rtype: None
        """
        docstring = getdoc(structure)
        if docstring is None or docstring.isspace():
            return
        return parse(docstring)
