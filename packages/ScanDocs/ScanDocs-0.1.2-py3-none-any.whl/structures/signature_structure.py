"""
The module containing the dataclass representing any structure that has a corresponding signature.
"""

from __future__ import annotations
from abc import ABC
from dataclasses import dataclass
from inspect import signature, Signature
from typing import TypeVar
from .source_structure import SourceStructure


StructureT = TypeVar("StructureT")


@dataclass(frozen=True, slots=True)
class SignatureStructure(SourceStructure[StructureT], ABC):
    """
    A structure that has a signature, such as a Python class or subroutine.
    """
    is_declared: bool
    signature: Signature | None

    @staticmethod
    def get_signature(structure: StructureT) -> Signature | None:
        """
        Gets the signature of a given structure, as provided by the in-built inspect API.

        :param structure: The given structure to get the signature from
        :return: The signature of the given structure
        :rtype: Signature
        :return: If the signature cannot be provided
        :rtype: None
        """
        try:
            return signature(structure)
        except ValueError:
            return  # Can't be provided
