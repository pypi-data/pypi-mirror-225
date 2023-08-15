"""
This module contains the tags that can be used to mark structures with particular details.

This contains the publicly accessible tags that are exposed to users,
so that subroutines can be marked in a particular way - this allows for the
documentation generator to provide details regarding the tagged subroutine as necessary.
"""

from __future__ import annotations
from dataclasses import dataclass
from .tag import Tag
from .data_tag import DataTag


@dataclass(frozen=True, slots=True)
class ContextManager(DataTag):
    """
    Mark a structure as a context manager.

    This indicates that the structure is designed to be used in a 'with' context statement,
    which is very difficult to determine internally without a dedicated tag.
    """
    is_async: bool = False

    def json_serialize(self) -> dict[str, object]:
        return {
            "isAsync": self.is_async
        }


@dataclass(frozen=True, slots=True)
class Deprecated(DataTag):
    """
    Mark a structure as deprecated.

    This indicates that the structure is now deprecated as of a specific version,
    and should no longer be used. It is recommended to include an alternative
    to using the tagged structure in the deprecation notice.
    """
    version: str
    description: str | None = None

    def json_serialize(self) -> dict[str, object]:
        return {
            "version": self.version,
            "description": self.description
        }


@dataclass(frozen=True, slots=True)
class Private(Tag):
    """
    Mark a structure as private.

    This indicates that the structure should not be documented when the
    website is generated. Variable names starting with a single underscore
    are treated in the same way.
    """


@dataclass(frozen=True, slots=True)
class Example(DataTag):
    """
    Add documented examples to a structure.
    """
    header: str
    python_code: str | None = None
    footer: str | None = None

    def json_serialize(self) -> dict[str, object]:
        return {
            "header": self.header,
            "code": self.python_code,
            "footer": self.footer
        }


@dataclass(frozen=True, slots=True)
class Link(DataTag):
    """
    Add relevant links to a structure's documentation.
    """
    title: str
    href: str
    description: str | None = None

    def json_serialize(self) -> dict[str, object]:
        return {
            "title": self.title,
            "href": self.href,
            "description": self.description
        }


@dataclass(frozen=True, slots=True)
class Note(DataTag):
    """
    Add relevant notes to a structure's documentation.
    """

    note: str

    def json_serialize(self) -> dict[str, object]:
        return {
            "note": self.note
        }
