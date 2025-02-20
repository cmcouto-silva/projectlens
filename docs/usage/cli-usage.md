# Command Line Interface (CLI) Usage

ProjectLens provides a powerful command-line interface for scanning and exporting project files.

## Command Overview

```bash
projectlens <folder_path> -x <extensions> [options]
```

## Required Arguments

| Argument | Description |
|---------|-------------|
| `<folder_path>` | Path to the project directory to scan |
| `-x, --extensions` | File extensions to include (e.g., `py md toml`) |

## Optional Arguments

| Option | Description |
|--------|-------------|
| `-i, --include` | Additional files to include regardless of extension |
| `-e, --exclude` | Patterns to exclude (supports glob patterns) |
| `-o, --output` | Custom output file path |
| `--max-file-size` | Maximum file size in KB (default: 1000) |
| `--ignore-file` | Path to custom ignore file (similar to .gitignore) |
| `--verbose` | Enable detailed debug logging |
| `--help` | Display help message |

## Examples

### Basic Usage

```bash
# Scan Python files
projectlens ~/myproject -x py

# Scan multiple file types
projectlens ~/myproject -x py md toml
```

### Including Specific Files

```bash
# Include Dockerfile and Makefile regardless of extension
projectlens ~/myproject -x py -i Dockerfile Makefile

# Include config files with your code
projectlens ~/myproject -x py js -i .env.example package.json
```

### Excluding Files and Directories

```bash
# Exclude tests directory
projectlens ~/myproject -x py md -e tests

# Exclude multiple patterns
projectlens ~/myproject -x py md -e tests docs "*cache*" "*.log"

# Exclude data folder and all .txt files
projectlens ~/myproject -x py md -e data "*txt"
```

### Output File Specification

```bash
# Custom output filename
projectlens ~/myproject -x py -o project_snapshot.txt

# Output to a different directory
projectlens ~/myproject -x py -o ~/outputs/project_analysis.txt
```

### File Size Limits

```bash
# Limit files to 500KB max
projectlens ~/myproject -x py --max-file-size 500

# Allow larger files (2000KB)
projectlens ~/myproject -x py --max-file-size 2000
```

### Custom Ignore File

```bash
# Use project-specific ignore file
projectlens ~/myproject -x py --ignore-file .customignore

# Use system-wide ignore configuration
projectlens ~/myproject -x py --ignore-file ~/global_ignores.txt
```

### Verbose Logging

```bash
# Enable detailed logging
projectlens ~/myproject -x py --verbose
```

## Understanding Output Messages

ProjectLens provides informative messages about the scanning process:

```
2025-02-20 04:10:07 - INFO - Starting to scan directory: /path/to/project
2025-02-20 04:10:07 - INFO - Writing contents to: project_snapshot.txt
2025-02-20 04:10:07 - INFO - Project Metadata
        Statistics
        ├── Scanned files: 10
        ├── Skipped directories: 1
        └── Skipped files (total=0)
            ├── Pattern matching: 0
            ├── Exceed file size: 0
            └── Failed: 0
2025-02-20 04:10:07 - SUCCESS - Successfully processed 10 files to project_snapshot.txt (3.9 KB).
```

With `--verbose` enabled, you'll see additional debug information:

```
2025-02-20 04:12:28 - DEBUG - Included file extensions: .bin, .py
2025-02-20 04:12:28 - DEBUG - Additional included files: Dockerfile
2025-02-20 04:12:28 - DEBUG - Exclude patterns: *$py.class, *.cover, ...
2025-02-20 04:12:28 - DEBUG - Maximum file size: 1,000 KB
2025-02-20 04:12:28 - DEBUG - Skipping __pycache__ due to pattern __pycache__
2025-02-20 04:12:28 - WARNING - Skipping large file: data/large_file.bin (1,500.0 KB)
```

## Default Ignore Patterns

ProjectLens automatically applies common ignore patterns (similar to .gitignore) to avoid including irrelevant files:

- Common build directories: `build/`, `dist/`, `__pycache__/`
- Virtual environments: `.venv/`, `env/`, `ENV/`
- Cache files: `.mypy_cache/`, `.pytest_cache/`, `*cache*/`
- Version control: `.git/`, `.hg/`
- Temporary files: `*.pyc`, `*.pyo`, `*.so`, `*.class`

You can view the complete list in the `.projectignore` file in the package.

## Exit Codes

- `0`: Successful execution
- `1`: Error occurred during execution

## Output Format

The generated output file will have the following structure:

```
Project Content Export
Generated on: 2025-02-20 06:29:10
Source directory: /path/to/project
Included file extensions: .md, .py, .toml
Additional included files: Dockerfile
Exclude patterns: __pycache__, *.pyc, ...

Project structure:
.
├── docs
│   ├── example.md
│   └── index.md
├── src
│   └── mymodule
│       ├── __init__.py
│       └── core.py
├── tests
│   ├── __init__.py
│   └── test_core.py
├── Dockerfile
└── README.md
================================================================================

File: README.md
--------------------------------------------------------------------------------
# Project Title
...
================================================================================

File: docs/example.md
--------------------------------------------------------------------------------
# Example Documentation
...
================================================================================
```

## Next Steps

- Learn how to use [Custom Ignore Files](configuration.md#custom-ignore-files)
- Explore the [Python API](python-api.md) for programmatic usage
- See [Advanced Usage](advanced-usage.md) for complex scenarios