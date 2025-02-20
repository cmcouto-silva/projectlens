"""Configuration management for ProjectLens.

This subpackage handles configuration settings for ProjectLens. It provides
functionality to load file/folder patterns to ignore, as well as a custom logger.

Exported names:
    load_ignore_patterns: Function to load file patterns to ignore (like .gitignore).
    logger: Pre-configured logger instance for the projectlens package.
"""

from projectlens.configs.config import load_ignore_patterns, logger

__all__ = ["load_ignore_patterns", "logger"]
