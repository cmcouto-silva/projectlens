"""Command Line Interface (CLI) for ProjectLens.

This module provides the command-line interface for the ProjectLens tool, allowing users
to export project files for analysis by Large Language Models (LLMs) like
ChatGPT, ClaudeAI, and DeepSeek.

The CLI supports various options for customizing the file collection process, including
specifying file extensions, including/excluding specific files or directories,
and setting maximum file size limits.

Example:
    Basic usage:
        $ projectlens . -x py md toml

    Including additional files, excluding folders, and naming output:
        $ projectlens . \
            -x py md toml \
            -i Dockerfile MakeFile \
            -e data tests "*txt"
            -o project_snapshopt.txt

    Enabling debugging details:
        $ projectlens . -x py yml -e data tests --verbose
"""

import argparse
import logging
import sys

from projectlens.configs import logger
from projectlens.core import ProjectLens


def main() -> int:
    """ProjectLens CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Export project files for LLM analysis."
    )

    parser.add_argument("folder_path", help="Path to the project directory")

    parser.add_argument(
        "-x",
        "--extensions",
        nargs="+",
        required=True,
        help="File extensions to include (e.g., py toml yml)",
    )

    parser.add_argument(
        "-i",
        "--include",
        nargs="+",
        default=[],
        help="Additional files to include",
    )

    parser.add_argument(
        "-e",
        "--exclude",
        nargs="+",
        default=[],
        help="Additional file and folders to exclude (supports glob patterns)",
    )

    parser.add_argument("-o", "--output", help="Output file path")

    parser.add_argument(
        "--max-file-size", type=int, default=None, help="Maximum file size in KB"
    )

    parser.add_argument("--ignore-file", help="Path to ignore file (like .gitignore)")

    parser.add_argument("--verbose", action="store_true", help="Enable debug details")

    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    try:
        project_lens = ProjectLens(
            extensions=args.extensions,
            include=args.include,
            exclude=args.exclude,
            ignore_file=args.ignore_file,
            max_file_size=args.max_file_size,
        )

        project_lens.export_project(folder_path=args.folder_path, output=args.output)
        return 0

    except Exception as e:
        logger.error(f"Error: {e!s}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
