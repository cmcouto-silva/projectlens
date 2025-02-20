"""Core module for ProjectLens.

This module provides functionalities for scanning, analyzing, and exporting
project file structures and contents based on specified configurations.

Classes:
    ProjectMetadata: Stores metadata related to scanned and skipped files.
    ProjectLens: Main class for scanning and exporting project file contents.
"""

import logging
import os
from dataclasses import dataclass, field
from datetime import datetime
from fnmatch import fnmatch
from pathlib import Path
from typing import Optional, Union

from projectlens.configs import load_ignore_patterns, logger
from projectlens.utils import bytes_to_kb, kb_to_bytes

logger.setLevel(logging.INFO)


@dataclass
class ProjectMetadata:
    """Stores metadata about scanned and skipped files during project analysis."""

    scanned_files: list[str] = field(default_factory=list)
    skipped_dirs: list[str] = field(default_factory=list)
    skipped_files: dict[str, list[str]] = field(
        default_factory=lambda: {
            "pattern_matching": [],
            "exceeded_size": [],
            "failed": [],
        }
    )

    def to_dict(self) -> dict:
        """Convert metadata into a dictionary format.

        Returns:
            dict: Dictionary containing metadata about scanned and skipped files.
        """
        return {
            "scanned_files": self.scanned_files,
            "skipped_dirs": self.skipped_dirs,
            "skipped_files": dict(self.skipped_files.items()),
        }

    def report_statistics(self) -> str:
        """Generate a summary report of the scanning process.

        Returns:
            str: Formatted summary of scanned and skipped files.
        """
        total_skipped_files = len(
            {v for values in self.skipped_files.values() for v in values}
        )
        skipped_pattern_matching = len(self.skipped_files["pattern_matching"])
        skipped_exceed_fsize = len(self.skipped_files["exceeded_size"])

        return (
            "\tStatistics\n"
            f"\t├── Scanned files: {len(self.scanned_files)}\n"
            f"\t├── Skipped directories: {len(self.skipped_dirs)}\n"
            f"\t└── Skipped files (total={total_skipped_files})\n"
            f"\t    ├── Pattern matching: {skipped_pattern_matching}\n"
            f"\t    ├── Exceed file size: {skipped_exceed_fsize}\n"
            f"\t    └── Failed: {len(self.skipped_files['failed'])}"
        )

    def report_inspection(self) -> str:
        """Generate a tree-structured debug log of project scan metadata.

        Returns:
            str:
                A formatted tree-structure string representation of the scan results.
        """

        def format_file_list(
            files: list[str], indent: str = "", is_last: bool = False
        ) -> str:
            if not files:
                return f"{indent}{'└── ' if is_last else '├── '}None"

            result = []
            for i, file in enumerate(files):
                is_file_last = i == len(files) - 1
                prefix = "└── " if is_file_last else "├── "
                result.append(f"{indent}{prefix}{Path(file)}")

            return "\n".join(result)

        tree = ["\tInspection"]

        # Scanned files section
        tree.append("\t├── Scanned files")
        tree.append(format_file_list(self.scanned_files, "\t│   "))

        # Skipped directories section
        tree.append("\t├── Skipped directories")
        tree.append(format_file_list(self.skipped_dirs, "\t│   "))

        # Skipped files categories
        tree.append("\t└── Skipped files")

        # Pattern matching files
        tree.append("\t    ├── Ignored files")
        tree.append(
            format_file_list(self.skipped_files["pattern_matching"], "\t    │   ")
        )

        # Exceeded size files
        tree.append("\t    ├── Exceeded size files")
        tree.append(format_file_list(self.skipped_files["exceeded_size"], "\t    │   "))

        # Failed files
        tree.append("\t    └── Failed files")
        tree.append(
            format_file_list(self.skipped_files["failed"], "\t        ", is_last=True)
        )

        return "\n".join(tree)


class ProjectLens:
    """Main class for scanning and exporting project files.

    Attributes:
        extensions (Set[str]): Set of file extensions to include.
        include (Optional[Set[str]]): Set of specific files to include.
        exclude (Optional[Set[str]]): Set of patterns to exclude.
        default_ignore (Optional[Set[str]])
        max_file_size (Optional[Union[int, float]]): Max file size in KB.
        metadata (ProjectMetadata): Stores scanning metadata.
    """

    def __init__(
        self,
        extensions: Union[list[str], set[str]],
        include: Optional[Union[list[str], set[str]]] = None,
        exclude: Optional[Union[list[str], set[str]]] = None,
        ignore_file: Optional[Union[Path, str]] = None,
        max_file_size: Optional[Union[int, float]] = 1000,
    ) -> None:
        """Initialize the ProjectLens scanner.

        Args:
            extensions (Union[List[str], Set[str]]):
                File extensions to include in scanning.
            include (Union[List[str], Set[str]], optional):
                Specific files to include. Defaults to None.
            exclude (Union[List[str], Set[str]], optional):
                Patterns to exclude. Defaults to None.
            ignore_file (Union[Path, str], optional):
                Path to file with default patterns to ignore (like .gitignore).
            max_file_size (Union[int, float], optional):
                Maximum file size in KB. Defaults to 1000.
        """
        self.extensions = self._normalize_extensions(extensions)
        self.include = set(include or set())
        self.default_ignore = load_ignore_patterns(ignore_file)
        self.exclude = set(exclude or set()) | self.default_ignore
        self.max_file_size = max_file_size or 1_000
        self.metadata = ProjectMetadata()

    @staticmethod
    def _normalize_extensions(extensions: Union[list[str], set[str]]) -> tuple[str]:
        """Normalize file extensions by converting them to lowercase and removing dots.

        Args:
            extensions (List[str]): List of file extensions.

        Returns:
            Tuple[str]: Normalized extensions.
        """
        extensions = tuple(ext.lower().lstrip(".") for ext in extensions)
        if not extensions:
            raise ValueError("No valid extensions provided")
        return extensions

    @staticmethod
    def _normalize_path(
        project_path: Union[str, Path], target_path: Union[str, Path]
    ) -> str:
        target_path = Path(target_path)
        project_path = Path(project_path).resolve()
        return str(target_path.relative_to(project_path))

    @staticmethod
    def _should_ignore(
        path: Union[str, Path], ignore_patterns: list[str], verbose: bool = True
    ) -> bool:
        path = Path(path)
        for ignore_pattern in ignore_patterns:
            if fnmatch(path.name, ignore_pattern):
                if verbose:
                    logger.debug(f"Skipping {path} due to pattern {ignore_pattern}")
                return True
        return False

    def _write(
        self,
        folder_path: Path,
        file_contents: dict[str, str],
        output_file: Optional[str] = None,
    ) -> None:
        """Write scanned file contents to an output file.

        Args:
            folder_path (Path): Root directory of the project.
            file_contents (Dict[str, str]): Dictionary of file paths and contents.
            output_file (str): Path to the output file.
        """
        logger.info(f"Writing contents to: {output_file}")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("Project Content Export\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Source directory: {folder_path}\n")
            f.write(
                "Included file extensions: "
                f"{', '.join(f'.{ext}' for ext in sorted(self.extensions))}\n"
            )
            if self.include:
                f.write(
                    f"Additional included files: {', '.join(sorted(self.include))}\n"
                )
            if self.exclude:
                f.write(f"Exclude patterns: {', '.join(sorted(self.exclude))}\n")

            f.write("Project structure:\n")
            f.write(".\n")
            f.write(self.generate_tree(folder_path, self.exclude))
            f.write("\n" + "=" * 80 + "\n\n")

            for file_path, content in sorted(file_contents.items()):
                f.write(f"File: {file_path}\n")
                f.write("-" * 80 + "\n")
                f.write(content)
                f.write("\n" + "=" * 80 + "\n\n")

        output_file_size = bytes_to_kb(Path(output_file).stat().st_size)
        logger.info("Project Metadata\n" + self.metadata.report_statistics())
        logger.success(
            f"Successfully processed {len(file_contents)} files to {output_file} "
            f"({output_file_size:,.1f} KB)."
        )

    def generate_tree(
        self,
        path: Union[str, Path],
        exclude: Optional[set[str]] = None,
        prefix: str = "",
    ) -> str:
        """Generate a tree-like representation of the directory structure.

        Parameters:
            path (Path):
                The root path to start generating the tree from.
            exclude (Set[str]):
                Set of directory names or patterns to exclude.
            prefix (str):
                Prefix for the current line (used for recursion).

        Returns:
            str: Tree-like string representation of the directory structure.
        """
        path = Path(path)
        exclude = exclude or set()

        tree = []
        entries = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name))

        for i, entry in enumerate(entries):
            is_last = i == len(entries) - 1
            node = "└──" if is_last else "├──"
            if entry.is_file() and not self._should_ignore(
                str(entry), exclude, verbose=False
            ):
                tree.append(f"{prefix}{node} {entry.name}")
            elif entry.is_dir() and not self._should_ignore(
                str(entry), exclude, verbose=False
            ):
                tree.append(f"{prefix}{node} {entry.name}")
                next_prefix = f"{prefix}{'    ' if is_last else '│   '}"
                tree.append(self.generate_tree(entry, exclude, next_prefix))

        return "\n".join(filter(None, tree))

    def export_project(
        self, folder_path: Union[str, Path], output: Optional[str] = None
    ) -> None:
        """Scan and export project files to an output file.

        Args:
            folder_path (Union[str, Path]): Root directory to scan.
            output (Optional[str], optional): Output file name. Defaults to None.
        """
        folder_path = Path(folder_path).resolve()

        if not folder_path.is_dir():
            raise FileNotFoundError(f"Directory not found: {folder_path}")

        if output is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M")
            output = f"{folder_path.name}_{timestamp}.txt"

        logger.debug(
            "Included file extensions: "
            f"{', '.join(f'.{ext}' for ext in sorted(self.extensions))}"
        )
        if self.include:
            logger.debug(
                f"Additional included files: {', '.join(sorted(self.include))}"
            )
        if self.exclude:
            logger.debug(f"Exclude patterns: {', '.join(sorted(self.exclude))}")

        logger.info(f"Starting to scan directory: {folder_path}")
        logger.debug(f"Maximum file size: {self.max_file_size:,} KB")
        file_contents = {}

        for dirpath, dirnames, filenames in os.walk(folder_path):
            skip_mask = [
                self._should_ignore(
                    self._normalize_path(folder_path, Path(dirpath) / Path(dirname)),
                    self.exclude,
                )
                for dirname in dirnames
            ]
            keep_dirs = [
                dirname for skip, dirname in zip(skip_mask, dirnames) if not skip
            ]
            skip_dirs = [dirname for skip, dirname in zip(skip_mask, dirnames) if skip]

            dirnames[:] = keep_dirs
            self.metadata.skipped_dirs.extend(
                [
                    self._normalize_path(folder_path, Path(dirpath) / Path(skip_dir))
                    for skip_dir in skip_dirs
                ]
            )

            for filename in filenames:
                file_path = Path(dirpath) / (filename)
                file_path_normalized = self._normalize_path(folder_path, file_path)

                if self._should_ignore(file_path_normalized, self.exclude):
                    self.metadata.skipped_files["pattern_matching"].append(
                        file_path_normalized
                    )
                    continue

                if filename.endswith(self.extensions) or filename in self.include:
                    file_size = file_path.stat().st_size
                    if file_size > kb_to_bytes(self.max_file_size):
                        logger.warning(
                            "Skipping large file: "
                            f"{file_path_normalized} ({bytes_to_kb(file_size):,.1f} KB)"
                        )
                        self.metadata.skipped_files["exceeded_size"].append(
                            file_path_normalized
                        )
                    else:
                        self.metadata.scanned_files.append(file_path_normalized)
                        try:
                            content = file_path.read_text(encoding="utf-8")
                            file_contents[file_path_normalized] = content
                        except Exception as e:
                            file_contents[file_path_normalized] = f"ERROR: {e!s}"
                            self.metadata.skipped_files["failed"].append(
                                file_path_normalized
                            )

        # Scan details if debug is True
        logger.debug("Project Inspection Details\n" + self.metadata.report_inspection())

        self._write(folder_path, file_contents, output)
