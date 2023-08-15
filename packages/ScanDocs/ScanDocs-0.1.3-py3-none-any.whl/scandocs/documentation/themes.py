"""
The module concerning the public API for customizing website themes.

This module contains the functionality behind customizable website themes before generation,
allowing for maximum generation flexibility - themes can be adjusted post-generation also.
"""

from enum import Enum


class Themes(Enum):
    """
    An enum containing all the in-built website themes that can be used.

    This enum allows for users to specify which of the default skeleton themes they would like
    to use during website generation. Themes can be easily changed after generation, but
    this provides a convenient way of generating documentation with a customizable theme with only the Python API.
    """
    SKELETON = "skeleton"
    MODERN = "modern"
    ROCKET = "rocket"
    SEAFOAM = "seafoam"
    VINTAGE = "vintage"
    SAHARA = "sahara"
    HAMLINDIGO = "hamlindigo"
    GOLD_NOUVEAU = "gold-nouveau"
    CRIMSON = "crimson"
