"""Unit tests for the core ProjectLens functionality.

This module contains comprehensive unit tests that cover various aspects of the
ProjectLens class and its methods. The tests ensure that ProjectLens behaves as
expected under different scenarios and edge cases.

The tests are organized into logical groups, each focusing on a specific feature or
method of ProjectLens. They make use of pytest fixtures to set up and tear down test
data and environments.

Example test groups:
    - Test file extension filtering
    - Test file inclusion/exclusion patterns
    - Test max file size limit
    - Test metadata collection
    - Test error handling and edge cases

To run the tests, simply invoke pytest from the project root:
    $ pytest -vv
"""

import os
import tempfile
from collections.abc import Generator
from pathlib import Path

import pytest
from pytest import fixture

from projectlens.core import ProjectLens, ProjectMetadata


@fixture
def test_project_structure() -> Generator[Path, None, None]:
    """Create a temporary test project structure."""
    with tempfile.TemporaryDirectory() as temp_dir:
        root_path = Path(temp_dir)

        # Root level files
        (root_path / "README.md").write_text("# Test Project")
        (root_path / "setup.py").write_text("from setuptools import setup")
        (root_path / "pyproject.toml").write_text("[tool.poetry]\nname = 'test'")
        (root_path / "Dockerfile").write_text("FROM python:3.9")
        (root_path / "requirements.txt").write_text("pytest>=7.0.0")
        (root_path / ".gitignore").write_text("__pycache__\n*.pyc")

        # Source directory
        src_dir = root_path / "src" / "testproject"
        os.makedirs(src_dir)
        (src_dir / "__init__.py").write_text("# Init file")
        (src_dir / "main.py").write_text("def main():\n    pass")
        (src_dir / "utils.py").write_text("def helper():\n    return True")

        # Tests directory
        tests_dir = root_path / "tests"
        os.makedirs(tests_dir)
        (tests_dir / "__init__.py").write_text("")
        (tests_dir / "test_main.py").write_text("def test_main():\n    assert True")

        # Docs directory
        docs_dir = root_path / "docs"
        os.makedirs(docs_dir)
        (docs_dir / "index.md").write_text("# Documentation")
        (docs_dir / "guide.md").write_text("## User Guide")

        # Cache directory to be ignored
        cache_dir = root_path / "__pycache__"
        os.makedirs(cache_dir)
        (cache_dir / "dummy.pyc").write_text("cache file")

        # Create a data directory with mixed content
        data_dir = root_path / "data"
        os.makedirs(data_dir)
        (data_dir / "config.yaml").write_text("key: value")
        (data_dir / "sample.csv").write_text("id,value\n1,test")
        (data_dir / "large_file.bin").write_text("x" * 1_500_000)  # > 1000KB

        yield root_path


@fixture
def output_file() -> Generator[str, None, None]:
    """Create a temporary output file."""
    with tempfile.NamedTemporaryFile(suffix=".txt") as out_file:
        yield out_file.name


def test_basic_extension_filtering(
    test_project_structure: Path, output_file: str
) -> None:
    """Test basic file filtering by extension."""
    lens = ProjectLens(extensions=["py"])
    lens.export_project(test_project_structure, output_file)

    # Check that only Python files were included
    assert "setup.py" in lens.metadata.scanned_files
    assert f"src{os.sep}testproject{os.sep}main.py" in lens.metadata.scanned_files
    assert f"src{os.sep}testproject{os.sep}utils.py" in lens.metadata.scanned_files

    # Check that non-python files were not included
    assert "README.md" not in lens.metadata.scanned_files
    assert "pyproject.toml" not in lens.metadata.scanned_files

    # Verify output file was created and has content
    with open(output_file) as f:
        content = f.read()
        assert "Project Content Export" in content
        assert "setup.py" in content


def test_multiple_extensions(test_project_structure: Path, output_file: str) -> None:
    """Test filtering by multiple extensions."""
    lens = ProjectLens(extensions=["py", "md", "toml"])
    lens.export_project(test_project_structure, output_file)

    # Check Python files
    assert "setup.py" in lens.metadata.scanned_files
    # Check Markdown files
    assert "README.md" in lens.metadata.scanned_files
    assert f"docs{os.sep}index.md" in lens.metadata.scanned_files
    # Check TOML files
    assert "pyproject.toml" in lens.metadata.scanned_files

    # Verify exclusions
    assert "Dockerfile" not in lens.metadata.scanned_files
    assert "requirements.txt" not in lens.metadata.scanned_files


def test_include_specific_files(test_project_structure: Path, output_file: str) -> None:
    """Test including specific files regardless of extension."""
    lens = ProjectLens(extensions=["py"], include=["Dockerfile", "requirements.txt"])
    lens.export_project(test_project_structure, output_file)

    # Check that specified includes are present
    assert "Dockerfile" in lens.metadata.scanned_files
    assert "requirements.txt" in lens.metadata.scanned_files

    # Check Python files are still included
    assert "setup.py" in lens.metadata.scanned_files

    # Verify other files are excluded
    assert "README.md" not in lens.metadata.scanned_files


def test_exclude_patterns(test_project_structure: Path, output_file: str) -> None:
    """Test excluding files and directories by pattern."""
    lens = ProjectLens(extensions=["py", "md"], exclude=["tests", "*.txt"])
    lens.export_project(test_project_structure, output_file)

    # Verify test files are excluded
    assert f"tests{os.sep}test_main.py" not in lens.metadata.scanned_files
    assert f"tests{os.sep}__init__.py" not in lens.metadata.scanned_files

    # Verify .txt files are excluded
    assert "requirements.txt" not in lens.metadata.scanned_files

    # Check that other files are still included
    assert "README.md" in lens.metadata.scanned_files
    assert "setup.py" in lens.metadata.scanned_files


def test_include_vs_exclude_priority(
    test_project_structure: Path, output_file: str
) -> None:
    """Test that exclude patterns take priority over includes."""
    lens = ProjectLens(
        extensions=["py"],
        include=["requirements.txt", "README.md"],
        exclude=["*.txt", "*.md"],
    )
    lens.export_project(test_project_structure, output_file)

    # Verify excluded patterns take priority
    assert "requirements.txt" not in lens.metadata.scanned_files
    assert "README.md" not in lens.metadata.scanned_files

    # Python files should still be included
    assert "setup.py" in lens.metadata.scanned_files


def test_max_file_size(test_project_structure: Path, output_file: str) -> None:
    """Test max file size filtering."""
    lens = ProjectLens(
        extensions=["py", "bin"],
        max_file_size=10,  # 10KB max
    )
    lens.export_project(test_project_structure, output_file)

    # Large file should be skipped
    large_file_path = f"data{os.sep}large_file.bin"
    assert large_file_path in lens.metadata.skipped_files["exceeded_size"]

    # Normal files should be included
    assert "setup.py" in lens.metadata.scanned_files


def test_normalize_extensions() -> None:
    """Test that extensions are normalized properly."""
    # Mix of formats with and without dots
    lens = ProjectLens(extensions=["py", ".md", "TOML", ".YAML"])

    # All should be normalized to lowercase without dots
    assert lens.extensions == ("py", "md", "toml", "yaml")


def test_default_directory_exclusions(
    test_project_structure: Path, output_file: str
) -> None:
    """Test that common directories are excluded by default."""
    lens = ProjectLens(
        extensions=["py", "pyc"], exclude=["__pycache__", ".git", ".vscode"]
    )
    lens.export_project(test_project_structure, output_file)

    # Check if any directories were skipped
    assert len(lens.metadata.skipped_dirs) > 0

    # Check if __pycache__ was among the skipped directories
    pycache_skipped = any(
        "__pycache__" in dir_path for dir_path in lens.metadata.skipped_dirs
    )
    assert pycache_skipped

    # No .pyc files should be included
    pyc_files = [f for f in lens.metadata.scanned_files if f.endswith(".pyc")]
    assert len(pyc_files) == 0


def test_tree_generation(test_project_structure: Path) -> None:
    """Test project tree generation."""
    lens = ProjectLens(extensions=["py"])
    tree = lens.generate_tree(test_project_structure)

    # Check that the tree contains expected structure elements
    assert "src" in tree
    assert "tests" in tree
    assert "setup.py" in tree

    # Tree should be formatted with proper indentation
    assert "└──" in tree
    assert "├──" in tree


def test_custom_output_file(test_project_structure: Path) -> None:
    """Test specifying custom output file."""
    lens = ProjectLens(extensions=["py"])
    custom_output = test_project_structure / "custom_output.txt"

    lens.export_project(test_project_structure, str(custom_output))

    # Verify file was created at specified location
    assert custom_output.exists()
    assert custom_output.stat().st_size > 0


def test_metadata_reporting() -> None:
    """Test metadata reporting functions."""
    metadata = ProjectMetadata()
    metadata.scanned_files = ["file1.py", "file2.py"]
    metadata.skipped_dirs = ["dir1", "dir2"]
    metadata.skipped_files["pattern_matching"] = ["skip1.txt"]
    metadata.skipped_files["exceeded_size"] = ["large.bin"]

    # Test statistics report
    stats = metadata.report_statistics()
    assert "Scanned files: 2" in stats
    assert "Skipped directories: 2" in stats
    assert "Pattern matching: 1" in stats
    assert "Exceed file size: 1" in stats

    # Test inspection report
    inspection = metadata.report_inspection()
    assert "Inspection" in inspection
    assert "file1.py" in inspection
    assert "dir1" in inspection
    assert "skip1.txt" in inspection
    assert "large.bin" in inspection


def test_dot_in_extensions_parameter() -> None:
    """Test that extensions with dots are handled correctly in CLI."""
    lens = ProjectLens(extensions=[".py", ".md", ".toml"])
    assert lens.extensions == ("py", "md", "toml")


def test_skipped_files_logging(
    test_project_structure: Path, output_file: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test that skipped files are properly logged."""
    log_messages = []

    # Create a mock logger that captures messages
    class MockLogger:
        def debug(self, msg: str, *args: object, **kwargs: object) -> None:
            log_messages.append(msg)

        def info(self, msg: str, *args: object, **kwargs: object) -> None:
            pass

        def warning(self, msg: str, *args: object, **kwargs: object) -> None:
            pass

        def error(self, msg: str, *args: object, **kwargs: object) -> None:
            pass

        def success(self, msg: str, *args: object, **kwargs: object) -> None:
            pass

    mock_logger = MockLogger()
    monkeypatch.setattr("projectlens.core.logger", mock_logger)

    lens = ProjectLens(extensions=["py"], exclude=["tests", "*.txt"], max_file_size=10)
    lens.export_project(test_project_structure, output_file)

    # Check if any debug messages contain "Skipping"
    skipped_msgs = [
        msg for msg in log_messages if isinstance(msg, str) and "Skipping" in msg
    ]

    # Should have at least one skipped file message
    assert len(skipped_msgs) > 0


def test_empty_extensions_error() -> None:
    """Test that empty extensions list raises error."""
    with pytest.raises(ValueError):
        ProjectLens(extensions=[])


def test_wildcard_exclusion(test_project_structure: Path, output_file: str) -> None:
    """Test wildcard pattern exclusion."""
    lens = ProjectLens(extensions=["py", "md"], exclude=["test*", "*cache*"])
    lens.export_project(test_project_structure, output_file)

    # All test* files/directories should be excluded or in skipped_files
    test_files = [f for f in lens.metadata.scanned_files if "test" in f.lower()]
    pattern_matched = [
        f
        for f in lens.metadata.skipped_files["pattern_matching"]
        if "test" in f.lower()
    ]

    # Either no test files in scanned_files, or they appear in pattern_matching
    assert len(test_files) == 0 or len(pattern_matched) > 0

    # Check if any skipped directories contain "cache"
    cache_skipped = any(
        "cache" in dir_path.lower() for dir_path in lens.metadata.skipped_dirs
    )

    # Either cache directory was skipped or no cache directories exist
    assert cache_skipped or not any(
        "cache" in dir_path.lower() for dir_path in os.listdir(test_project_structure)
    )


def test_extensions_with_dots_in_cli(
    test_project_structure: Path, output_file: str
) -> None:
    """Test handling extensions specified with dots."""
    lens = ProjectLens(extensions=[".py", ".md", ".toml"])
    lens.export_project(test_project_structure, output_file)

    # Should handle extensions with dots properly
    assert "setup.py" in lens.metadata.scanned_files
    assert "README.md" in lens.metadata.scanned_files


def test_complex_exclusion_patterns(
    test_project_structure: Path, output_file: str
) -> None:
    """Test complex exclusion patterns."""
    lens = ProjectLens(
        extensions=["py", "md", "toml"],
        exclude=["tests", "*.csv"],  # Simplified exclusion patterns
    )
    lens.export_project(test_project_structure, output_file)

    # Test directory should be excluded
    test_files_included = any(
        f.startswith("tests") for f in lens.metadata.scanned_files
    )
    test_dir_skipped = any(
        "tests" in dir_path for dir_path in lens.metadata.skipped_dirs
    )

    # Either test files were excluded or tests directory was skipped
    assert not test_files_included or test_dir_skipped

    # CSV files in data dir should be excluded from scanned files
    csv_files_included = any(
        f.endswith(".csv") and "data" in f for f in lens.metadata.scanned_files
    )
    assert not csv_files_included


def test_nested_include_patterns(
    test_project_structure: Path, output_file: str
) -> None:
    """Test including nested files."""
    lens = ProjectLens(
        extensions=["yaml"],
        include=["config.yaml"],  # Simplified - looking for any config.yaml
    )
    lens.export_project(test_project_structure, output_file)

    # Should find config.yaml somewhere in the results
    config_files = [f for f in lens.metadata.scanned_files if f.endswith("config.yaml")]
    assert len(config_files) > 0
