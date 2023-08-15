"""
The module containing the dataclass that represents a serialized node, ready to be converted to JSON.
"""

from __future__ import annotations
from dataclasses import dataclass


JsonT = dict[str, str | dict[str, object] | list[dict[str, "JsonT"]]]


@dataclass(frozen=True, slots=True)
class Serialized:
    """
    The dataclass that represents a serialized node, ready to be converted to JSON.
    """
    component: str
    meta: dict[str, object]
    children: dict[str, list[Serialized]]

    def to_json(self) -> JsonT:
        """
        Converts this object into a JSON tree.

        A method that converts this node, and its children into a compatible JSON format recursively,
        so that it can be used in the website.

        :return: The JSON tree of structures to be used in the website
        """
        return {
            "component": self.component,
            "meta": self.meta,
            "children": {
                child_type: [child.to_json() for child in self.children[child_type]] for child_type in self.children
            }
        }
