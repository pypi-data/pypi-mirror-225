"""
The module containing the dataclass representing deprecation notices in a Python docstring.

The dataclass contained in this module has been deprecated in favour of using Deprecation markers.
Deprecation notices in package or module level docstrings should be placed in the docstring description.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Callable
from docstring_parser import DocstringDeprecated
from .serialized import Serialized
from .structure import Structure
from ..tags import Deprecated, Link


@Deprecated(
    "v0.1.1",
    "Deprecated in favour of using tags to indicate deprecation, as it is considered to be more robust"
)
@dataclass(frozen=True, slots=True)
class Deprecation(Structure):
    """
    The dataclass representing deprecation notices in a Python docstring.

    This class is deprecated, but is still used to store deprecation details -
    this information is not used by default in the website generation.
    """
    description: str
    version: str

    @classmethod
    @Link(
        "Docstring Parser API", "https://pypi.org/project/docstring-parser/",
        "The API that provides the DocstringDeprecated objects this method uses."
    )
    def from_docstring_deprecated(cls, deprecation: DocstringDeprecated) -> Deprecation:
        """
        Forms an instance of this class from a DocstringDeprecated object.

        This class method is used to form instances of this class from DocstringDeprecated objects,
        as provided by the Docstring Parser API.

        :param deprecation: The object to form a new object from
        :return: A corresponding instance of this class
        """
        return cls(
            deprecation.description,
            deprecation.version
        )

    def serialize(self, child_filter: Callable[[Structure], bool] = lambda _: True) -> Serialized:
        return Serialized(
            "Deprecation",
            {
                "description": self.description,
                "version": self.version
            },
            {}
        )
