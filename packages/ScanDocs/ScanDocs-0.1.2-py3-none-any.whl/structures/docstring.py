"""
The module containing the dataclass representing Python docstrings.
"""

from __future__ import annotations
from dataclasses import dataclass
from docstring_parser import Docstring as ParserDocstring
from .parameter import Parameter
from .error import Error
from .subroutine_return import SubroutineReturn
from .deprecation import Deprecation
from ..tags import Link


@dataclass(frozen=True, slots=True)
class Docstring:
    """
    The dataclass representing Python docstrings.
    """
    short_description: str
    long_description: str
    deprecation: Deprecation | None
    parameters: list[Parameter]
    raises: list[Error]
    returns: list[SubroutineReturn]

    @classmethod
    @Link(
        "Docstring Parser API", "https://pypi.org/project/docstring-parser/",
        "The API that provides the Docstring objects this method uses."
    )
    def from_docstring(cls, docstring: ParserDocstring, return_annotation: str | None = None) -> Docstring:
        """
        Forms an instance of this class from an external Docstring object.

        This class method is used to form instances of this class from Docstring objects,
        as provided by the Docstring Parser API.

        :param docstring: The object to form a new object from
        :param return_annotation: The return annotation of the corresponding subroutine, if applicable
        :return: A corresponding instance of this class
        """
        return cls(
            docstring.short_description,
            docstring.long_description,
            Deprecation.from_docstring_deprecated(docstring.deprecation) if docstring.deprecation else None,
            [Parameter(
                parameter.arg_name,
                parameter.description,
                parameter.type_name,
                parameter.default,
                parameter.is_optional
            ) for parameter in docstring.params],
            [Error.from_docstring_raises(error) for error in docstring.raises],
            [SubroutineReturn.from_docstring_returns(
                subroutine_return
            ).patch_annotation(return_annotation) for subroutine_return in docstring.many_returns]
        )
