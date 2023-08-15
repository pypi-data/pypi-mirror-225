"""
A module containing the documentation configuration API.

This module contains the public API allowing users to configure their website
before it is generated, to maximise simplicity.
"""

from dataclasses import dataclass
from .themes import Themes


@dataclass(frozen=True, slots=True)
class Configuration:
    """
    A dataclass for customizing details of the generated website.

    This dataclass provides a straightforward way to configure various options for ScanDocs documentation.
    It can be used to personalize the appearance of the website easily, allowing for maximum adaptibility
    before the website is ever generated.
    """
    project_name: str
    theme: Themes = Themes.SKELETON
    search_placeholder: str = "Search Documentation..."
    json_indent: int = 4
