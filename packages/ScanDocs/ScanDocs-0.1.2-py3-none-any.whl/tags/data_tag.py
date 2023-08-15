"""
A module containing internal details for how data tags are structured.
"""

from dataclasses import dataclass
from abc import ABC, abstractmethod
from .tag import Tag


@dataclass(frozen=True, slots=True)
class DataTag(Tag, ABC):
    """
    A particular type of tag that requires serialization.

    This is used when the tag holds valuable information that is required in the website.
    """

    @abstractmethod
    def json_serialize(self) -> dict[str, object]:
        """
        Serialize the tag, so that it can be used in the website.

        This method must be implemented by children tags, and is used to
        serialize the information provided by the tag into a JSON compatible
        dictionary, so that it can be used appropriately in the documentation website.

        :return: The serialized information as a JSON compatible dictionary
        """
        ...
