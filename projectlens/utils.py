"""Utility functions for ProjectLens.

This module provides helper functions for file size conversion and other utility
operations used throughout the ProjectLens project.

Functions:
    bytes_to_kb: Convert bytes to kilobytes.
    kb_to_bytes: Convert kilobytes to bytes.
"""


def bytes_to_kb(bytes_size: int) -> float:
    """Convert bytes to kilobytes.

    Args:
        bytes_size (int): Size in bytes.

    Returns:
        float: Size in kilobytes.
    """
    return bytes_size / (1000)


def kb_to_bytes(kb: int) -> int:
    """Convert kilobytes to bytes.

    Args:
        kb (int): Size in kilobytes.

    Returns:
        int: Size in bytes.
    """
    return kb * 1000
