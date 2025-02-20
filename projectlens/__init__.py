"""The top-level package for ProjectLens.

This package provides the main entry point to the ProjectLens API. Users can import the
ProjectLens class directly from this package to access all core functionality.

Example usage:
    >>> from projectlens import ProjectLens
    >>> lens = ProjectLens(extensions=["py", "md"])
    >>> lens.export_project("path/to/project")

Exported names:
    ProjectLens: The main ProjectLens class for scanning and exporting projects.
"""
from projectlens.core import ProjectLens

__version__ = "0.0.1"

__all__ = [ProjectLens]
