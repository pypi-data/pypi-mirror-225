"""
The module containing the dataclass representing return (or yield) information from Python subroutines.
"""

from __future__ import annotations
from dataclasses import dataclass
from inspect import Signature
from typing import Callable
from docstring_parser import DocstringReturns
from .serialized import Serialized
from .structure import Structure
from ..tags import Link


@dataclass(frozen=True, slots=True)
class SubroutineReturn(Structure):
    """
    The dataclass representing return (or yield) information from Python subroutines.
    """
    description: str
    annotation: str | None

    @classmethod
    @Link(
        "Docstring Parser API", "https://pypi.org/project/docstring-parser/",
        "The API that provides the DocstringReturns objects this method uses."
    )
    def from_docstring_returns(cls, returns: DocstringReturns) -> SubroutineReturn:
        """
        Forms an instance of this class from a DocstringReturns object.

        This class method is used to form instances of this class from DocstringReturns objects,
        as provided by the Docstring Parser API.

        :param returns: The object to form a new object from
        :return: A corresponding instance of this class
        """
        return cls(
            returns.description,
            returns.type_name
        )

    def patch_annotation(self, annotation: str) -> SubroutineReturn:
        """
        Overwrites the existing annotation of this object with a new one

        An internal utility method to overwrite the existing annotation attribute
        of this object with a new one, bypassing this class' frozen nature.

        :param annotation: The new replacement annotation
        :return: The modified instance of this class
        """
        if annotation != "":
            object.__setattr__(self, "annotation", annotation)
        return self

    def serialize(self, child_filter: Callable[[Structure], bool] = lambda _: True) -> Serialized:
        return Serialized(
            "SubroutineReturn",
            {
                "description": self.description,
                "annotation": self.annotation
            },
            {}
        )

    @staticmethod
    def get_annotation(annotation: object) -> str | None:
        """
        Writes a given annotation in a more easily readable format.

        :param annotation: The given annotation
        :return: A readable string representation of the annotation
        :rtype: str
        :return: If no annotation exists on the corresponding structure
        :rtype: None
        """
        if annotation in (Signature.empty, "_empty"):
            return
        return annotation.__name__ if isinstance(annotation, type) else str(annotation)
