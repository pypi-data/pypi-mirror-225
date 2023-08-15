"""
An internal module containing the dataclass which simplifies file contents replacement logic.
"""

from dataclasses import dataclass


@dataclass
class Replacement:
    """
    A simple dataclass representing content replacements between files.

    An internal dataclass containing details about replacements made
    between files during the website generation process, to simplify the API.
    """
    marker: str
    content: str
