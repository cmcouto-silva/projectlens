"""Configuration management for ProjectLens.

This module handles loading and management of configuration settings for ProjectLens.
It provides functionality to load ignore patterns from .projectignore files and supports
custom SUCCESS level logging for better visibility of successful operations.

Functions:
    load_ignore_patterns: Load ignore patterns from .projectignore files.
    success: Custom logging method for SUCCESS-level messages.
"""

import logging
from importlib import resources
from pathlib import Path
from typing import Optional, Union

import projectlens.configs

# Configure logging
SUCCESS = 25
logging.addLevelName(SUCCESS, "SUCCESS")


def success(
    self: logging.Logger, message: object, *args: object, **kwargs: object
) -> None:
    """Log a message with the custom SUCCESS level."""
    self.log(SUCCESS, message, *args, **kwargs)


logging.Logger.success = success

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("projectlens")


def load_ignore_patterns(ignore_file: Optional[Union[str, Path]] = None) -> set[str]:
    """Load ignore patterns from `.projectignore`.

    The function checks for ignore patterns in the following order:
    1. If `ignore_file` is explicitly provided, load patterns from that file.
    2. Otherwise, check for a `.projectignore` file in the current execution directory.
    3. If not found, fall back to the default `.projectignore` in `projectlens/configs`.

    Args:
        ignore_file (Optional[Union[str, Path]]): Path to a custom ignore file.

    Returns:
        Set[str]: A set of ignore patterns.
    """
    ignore_patterns = set()

    # If the user provides an explicit ignore file, use it
    if ignore_file:
        ignore_path = Path(ignore_file)
    else:
        # Look for `.projectignore` in the current working directory
        cwd_ignore = Path.cwd() / ".projectignore"
        ignore_path = cwd_ignore if cwd_ignore.exists() else None

        # Fallback to default `.projectignore` in projectlens/configs/
        if ignore_path is None:
            ignore_path = resources.files(projectlens.configs).joinpath(
                ".projectignore"
            )

    # Load patterns if the file exists
    try:
        with open(ignore_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):  # Ignore comments
                    ignore_patterns.add(line.strip("/"))
    except Exception:
        raise

    return ignore_patterns
