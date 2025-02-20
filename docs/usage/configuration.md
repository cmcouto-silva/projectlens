# Configuration Options

ProjectLens offers various configuration options to customize its behavior. This page explains the available configuration methods and how to use them effectively.

## Configuration Methods

ProjectLens can be configured through:

1. Command-line arguments
2. Custom ignore files
3. Python API parameters

## File Extensions

File extensions determine which types of files ProjectLens will scan and include in the output.

### CLI Example

```bash
# Scan only Python files
projectlens /path/to/project -x py

# Scan multiple file types
projectlens /path/to/project -x py js ts md yaml
```

### Python API Example

```python
# Single extension
lens = ProjectLens(extensions=["py"])

# Multiple extensions
lens = ProjectLens(extensions=["py", "js", "md", "yaml", "toml"])
```

### Notes

- Extensions can be specified with or without the leading dot (both `py` and `.py` work)
- All extensions are normalized to lowercase internally
- At least one extension must be specified
- Empty extension lists will raise a ValueError

## Include Patterns

Include patterns let you specify files to include regardless of their extension.

### CLI Example

```bash
# Include Dockerfile and Makefile
projectlens /path/to/project -x py -i Dockerfile Makefile

# Include configuration files
projectlens /path/to/project -x py -i .env .dockerignore config.json
```

### Python API Example

```python
lens = ProjectLens(
    extensions=["py"],
    include=["Dockerfile", "Makefile", ".env"]
)
```

### Notes

- Include patterns are exact filename matches, not glob patterns
- Files matching include patterns will be included even if they don't match any extensions
- Include patterns are case-sensitive
- Include patterns are evaluated after extension matching

## Exclude Patterns

Exclude patterns let you specify files and directories to exclude from scanning.

### CLI Example

```bash
# Exclude tests directory
projectlens /path/to/project -x py -e tests

# Exclude multiple patterns
projectlens /path/to/project -x py -e tests docs "*cache*" "*.log"
```

### Python API Example

```python
lens = ProjectLens(
    extensions=["py"],
    exclude=["tests", "docs", "*cache*", "*.log"]
)
```

### Notes

- Exclude patterns support glob-style wildcards (`*`, `?`)
- Exclude patterns take precedence over include patterns
- Patterns can match directories or files
- When a directory is excluded, all its contents are skipped
- Exclude patterns are case-sensitive on case-sensitive filesystems

## Custom Ignore Files

ProjectLens can use a `.projectignore` file (similar to `.gitignore`) to specify patterns to exclude.

### Creating a Custom Ignore File

Create a file named `.projectignore` in your project directory:

```
# Comment - this line is ignored
__pycache__/
*.pyc
*.pyo
build/
dist/
.venv/
node_modules/
*.log
```

### Specifying a Custom Ignore File

#### CLI Example

```bash
projectlens /path/to/project -x py --ignore-file .customignore
```

#### Python API Example

```python
from pathlib import Path

lens = ProjectLens(
    extensions=["py"],
    ignore_file=Path("/path/to/.customignore")
)
```

### Ignore File Resolution

ProjectLens looks for ignore patterns in the following order:

1. If `ignore_file` is explicitly provided, load patterns from that file
2. Look for a `.projectignore` file in the current working directory
3. Fall back to the default `.projectignore` in the package

## Maximum File Size

You can limit the size of files to be included in the output.

### CLI Example

```bash
# Limit to 500KB
projectlens /path/to/project -x py --max-file-size 500

# No size limit
projectlens /path/to/project -x py --max-file-size 0
```

### Python API Example

```python
# 500KB limit
lens = ProjectLens(
    extensions=["py"],
    max_file_size=500
)

# Default limit (1000KB)
lens = ProjectLens(
    extensions=["py"]
)

# Uses default size limit (1000KB)
lens = ProjectLens(
    extensions=["py"],
    max_file_size=None
)
```
