# ProjectLens 🔍

![Tests](https://github.com/cmcouto-silva/projectlens/actions/workflows/test.yml/badge.svg)
[![codecov](https://codecov.io/gh/cmcouto-silva/projectlens/branch/main/graph/badge.svg)](https://codecov.io/gh/cmcouto-silva/projectlens)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A powerful tool for collecting and analyzing coding project files for review and optimization with Large Language Models (LLMs) like ChatGPT, Claude, DeepSeek, and other AI assistants.

## Overview

ProjectLens scans your codebase and creates a comprehensive text export that you can feed directly to AI models. It intelligently filters files based on extensions, respects common ignore patterns, and creates a well-formatted output that maximizes the context available to LLMs.

## Features

- 🔍 Recursively collect project files with specified extensions and smart filtering
- 🌲 Generate detailed project tree structure 
- 📝 Create well-formatted output optimized for LLM analysis
- 🚀 Easy to use as both CLI tool and Python API
- 🛠️ Zero external dependencies

## Installation

```bash
pip install projectlens
```

For development installation:

```bash
git clone https://github.com/cmcouto-silva/projectlens
cd projectlens
uv sync  # or pip install -e .
```

## Quick Start

### CLI Usage

```bash
# Basic usage - scan Python, Markdown and TOML files
projectlens /path/to/project -x py md toml

# Include specific files regardless of extension
projectlens /path/to/project -x py -i Dockerfile Makefile

# Exclude specific directories or patterns
projectlens /path/to/project -x py md -e tests *cache*

# Specify output file
projectlens /path/to/project -x py -o project_snapshot.txt

# Get detailed logs
projectlens /path/to/project -x py md -e data tests --verbose
```

### Python API Usage

```python
from projectlens import ProjectLens

# Initialize with file extensions to include
lens = ProjectLens(
    extensions=["py", "md", "toml"],
    include=["Dockerfile"],          # Additional files to include
    exclude=["tests", "*cache*"],    # Patterns to exclude
    max_file_size=500                # Maximum file size in KB
)

# Export the project
lens.export_project(
    folder_path="/path/to/project",
    output="project_snapshot.txt"    # Optional, auto-generated if not specified
)
```

## Documentation

For detailed documentation, visit our [documentation site](https://cmcouto-silva.github.io/projectlens/).

## Use Cases

- **LLM Code Review**: Generate a complete snapshot of your project for AI review
- **Documentation Generation**: Have AI analyze your project structure to suggest documentation
- **Knowledge Transfer**: Help new team members understand project structure
- **Legacy Code Understanding**: Analyze unfamiliar codebases quickly

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits

Created and maintained by [Cainã Max Couto da Silva](https://github.com/cmcouto-silva).

## Donate

Like it? Consider [buying me a coffee](buymeacoffee.com/cmcoutosilva) (don't forget the message) 😊