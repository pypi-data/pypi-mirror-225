"""
The module containing the dataclass representing any structure that can be searched for on the generated website.
"""

from __future__ import annotations
from dataclasses import dataclass
from abc import ABC, abstractmethod
from .structure import Structure


@dataclass(frozen=True, slots=True)
class SearchableStructure(Structure, ABC):
    """
    A structure that can be searched for on the generated website.
    """

    @property
    @abstractmethod
    def search_terms(self) -> str:
        """
        A dynamic property defining the terms that this structure can be searched for with.

        This property is used by the website files to search for searchable structures in the project.

        :return: A string of terms that this structure can be searched for with
        """
        ...

    @property
    @abstractmethod
    def search_category(self) -> str:
        """
        A dynamic property defining what category this searchable structure is listed as.

        This property is used by the website files when filtering searches between categories.

        :return: The name of the search category
        """
        ...
