"""
Dataclasses to interface with projects.

This package includes the functionality behind scanning a python project.
It allows for structures (such as classes) in a codebase to be interfaced with in a consistent manner,
and provides tooling such as serialization, whilst storing only the necessary information
about each structure in a scanned codebase, to minimize build times.
"""


from .class_ import Class
from .module import Module
from .package import Package
from .subroutine import Subroutine
from .structure import Structure
from .source_structure import SourceStructure
from .signature_structure import SignatureStructure
from .searchable_structure import SearchableStructure
