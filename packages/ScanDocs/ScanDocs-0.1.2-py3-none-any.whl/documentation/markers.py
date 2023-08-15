"""
An internal module containing markers for website generation.
"""

from enum import Enum


class Markers(Enum):
    """
    Contains all the markers where code from ScanDocs templates may be placed.

    This is an internal enum that holds the different markers for where
    content is copied between files during website generation.
    """
    PROJECT = "\"%PROJECT_HERE%\""
    PROJECT_NAME = "\"%PROJECT_NAME_HERE%\""
    THEME = "\"%THEME_HERE%\""
