"""
Exposed API utilities for detailed code beyond the capability of docstrings.

This package includes the available tags that users can interact with, allowing for further information
to be passed to the program about different structures, beyond the capability of docstrings.
This includes functionality such as deprecation notices.
"""


from .tags import ContextManager, Deprecated, Private, Example, Link, Note
from .tag import Tag
