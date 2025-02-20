# Python API Reference

ProjectLens provides a clean Python API that allows you to integrate project scanning functionality into your own scripts and applications.

## Getting Started

To use ProjectLens as a Python library, first import the main class:

```python
from projectlens import ProjectLens
```

## ProjectLens Class

The `ProjectLens` class is the main entry point for programmatic usage of ProjectLens.

### Constructor

```python
ProjectLens(
    extensions: Union[list[str], set[str]],
    include: Optional[Union[list[str], set[str]]] = None,
    exclude: Optional[Union[list[str], set[str]]] = None,
    ignore_file: Optional[Union[Path, str]] = None,
    max_file_size: Optional[Union[int, float]] = 1000,
)
```

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `extensions` | `List[str]` or `Set[str]` | File extensions to include (without or with leading dot) |
| `include` | `List[str]` or `Set[str]` (optional) | Specific files to include regardless of extension |
| `exclude` | `List[str]` or `Set[str]` (optional) | Patterns to exclude (supports glob patterns) |
| `ignore_file` | `Path` or `str` (optional) | Path to custom ignore file |
| `max_file_size` | `int` or `float` (optional) | Maximum file size in KB (default: 1000) |

### Methods

#### export_project

```python
export_project(
    folder_path: Union[str, Path],
    output: Optional[str] = None
) -> None
```

Scans a project directory and exports the results to a file.

##### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `folder_path` | `str` or `Path` | Root directory to scan |
| `output` | `str` (optional) | Output file path. If not specified, auto-generates a filename based on directory name and timestamp |

##### Exceptions

- `FileNotFoundError`: If the specified directory doesn't exist
- `ValueError`: If no valid extensions are provided
- Various I/O exceptions may be raised during file operations

#### generate_tree

```python
generate_tree(
    path: Union[str, Path],
    exclude: Optional[set[str]] = None,
    prefix: str = ""
) -> str
```

Generates a tree-like representation of the directory structure.

##### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `path` | `str` or `Path` | The root path to start generating the tree from |
| `exclude` | `Set[str]` (optional) | Set of directory names or patterns to exclude |
| `prefix` | `str` (optional) | Prefix for the current line (used for recursion) |

##### Returns

A string containing the tree representation of the directory structure.

### Attributes

After scanning a project, the following attributes are available:

| Attribute | Type | Description |
|-----------|------|-------------|
| `extensions` | `Tuple[str]` | Normalized file extensions (lowercase, no dots) |
| `include` | `Set[str]` | Set of specific files to include |
| `exclude` | `Set[str]` | Set of patterns to exclude |
| `default_ignore` | `Set[str]` | Default ignore patterns |
| `max_file_size` | `int` or `float` | Maximum file size in KB |
| `metadata` | `ProjectMetadata` | Metadata about scanned/skipped files |

## ProjectMetadata Class

The `ProjectMetadata` class stores information about the scanning process.

### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `scanned_files` | `List[str]` | List of successfully scanned files |
| `skipped_dirs` | `List[str]` | List of skipped directories |
| `skipped_files` | `Dict[str, List[str]]` | Dictionary containing skipped files by reason |

The `skipped_files` dictionary has the following keys:
- `pattern_matching`: Files skipped due to exclude patterns
- `exceeded_size`: Files skipped because they exceed the maximum size
- `failed`: Files that failed to be read

### Methods

#### to_dict

```python
to_dict() -> dict
```

Converts the metadata to a dictionary format.

#### report_statistics

```python
report_statistics() -> str
```

Generates a summary report of the scanning process.

#### report_inspection

```python
report_inspection() -> str
```

Generates a tree-structured debug log of project scan metadata.

## Examples

### Basic Usage

```python
from projectlens import ProjectLens

# Initialize with Python and Markdown files
lens = ProjectLens(extensions=["py", "md"])

# Scan and export a project
lens.export_project(folder_path="/path/to/project")
```

### Advanced Configuration

```python
from projectlens import ProjectLens
from pathlib import Path

# Initialize with custom configuration
lens = ProjectLens(
    extensions=["py", "js", "md"],
    include=["Dockerfile", "package.json", ".env.example"],
    exclude=["tests", "docs", "*cache*", "*.min.js"],
    ignore_file=Path.home() / ".projectignore",
    max_file_size=500
)

# Export with custom output path
lens.export_project(
    folder_path="/path/to/myproject",
    output="/path/to/outputs/myproject_scan.txt"
)
```

### Accessing Scan Metadata

```python
from projectlens import ProjectLens

lens = ProjectLens(extensions=["py"])
lens.export_project("/path/to/project")

# Access metadata after scanning
print(f"Files scanned: {len(lens.metadata.scanned_files)}")
print(f"Directories skipped: {len(lens.metadata.skipped_dirs)}")
print(f"Files skipped due to size: {len(lens.metadata.skipped_files['exceeded_size'])}")

# Get detailed statistics
stats_report = lens.metadata.report_statistics()
print(stats_report)

# Convert metadata to dictionary
metadata_dict = lens.metadata.to_dict()
```

### Generating Directory Tree

```python
from projectlens import ProjectLens
from pathlib import Path

lens = ProjectLens(extensions=["py"])
project_path = Path("/path/to/project")

# Generate tree representation
tree = lens.generate_tree(
    project_path,
    exclude={"__pycache__", ".git", "venv"}
)

print(tree)
```

### Error Handling

```python
from projectlens import ProjectLens
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

try:
    lens = ProjectLens(extensions=["py"])
    lens.export_project("/path/to/nonexistent/directory")
except FileNotFoundError as e:
    logging.error(f"Directory not found: {e}")
except Exception as e:
    logging.error(f"An error occurred: {e}")
```

## Best Practices

1. **Extension Formatting**: Extensions can be specified with or without the leading dot (`.py` or `py`)
2. **Use Glob Patterns**: For exclude patterns, use glob patterns for more flexible matching
3. **Metadata Access**: Always access metadata after calling `export_project()`
4. **Path Objects**: Both string paths and `pathlib.Path` objects are supported
5. **Custom Ignores**: Create project-specific ignore files for consistent filtering

## Next Steps

- Learn about [Configuration Options](configuration.md)
- Explore [Advanced Usage Patterns](advanced-usage.md)
- See [Use Cases](../guides/use-cases.md) for practical applications