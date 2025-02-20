# Quick Start Guide

This guide will help you get up and running with ProjectLens quickly. We'll cover basic usage patterns for both the command-line interface and Python API.

## Basic CLI Usage

The simplest way to use ProjectLens is through its command-line interface:

```bash
projectlens <folder_path> -x <extensions>
```

Where:
- `<folder_path>` is the path to your project directory
- `-x <extensions>` specifies which file extensions to include (required)

### Example: Basic Scanning

Scan a project for Python, Markdown, and TOML files:

```bash
projectlens ~/myproject -x py md toml
```

This will:
1. Scan all files with `.py`, `.md`, and `.toml` extensions
2. Generate a tree structure of your project
3. Create an output file named `myproject_YYYYMMDD_HHMM.txt`

### Example: Including Specific Files

Include additional files regardless of their extension:

```bash
projectlens ~/myproject -x py -i Dockerfile Makefile .env.example
```

### Example: Excluding Patterns

Exclude specific directories or file patterns:

```bash
projectlens ~/myproject -x py md -e tests docs "*cache*"
```

### Example: Custom Output File

Specify your own output filename:

```bash
projectlens ~/myproject -x py -o project_for_llm_review.txt
```

### Example: Verbose Mode

Get detailed information about what's being processed:

```bash
projectlens ~/myproject -x py --verbose
```

## Basic Python API Usage

You can also use ProjectLens programmatically in your Python scripts:

```python
from projectlens import ProjectLens

# Initialize the scanner
lens = ProjectLens(
    extensions=["py", "md", "yml"],
    include=["Dockerfile", ".gitignore"],
    exclude=["tests", "build", "*cache*"],
    max_file_size=500  # in KB
)

# Scan and export project
lens.export_project(
    folder_path="/path/to/project",
    output="project_snapshot.txt"  # Optional
)

# Access metadata about the scan
print(f"Files scanned: {len(lens.metadata.scanned_files)}")
print(f"Directories skipped: {len(lens.metadata.skipped_dirs)}")
```

## Understanding the Output

ProjectLens generates a single text file containing:

1. **Header information**:
   - Generation timestamp
   - Source directory
   - Included file extensions
   - Exclude patterns

2. **Project tree structure**:
   - Visual representation of your project's directory hierarchy
   
3. **File contents**:
   - Each file's content with clear separation and formatting
   - Consistent headers and separators for easy parsing

## Using Output with LLMs

The output is specifically formatted to be easily parsed by Large Language Models (LLMs). To use it:

1. Upload the generated file into your LLM chat (ChatGPT, ClaudeAI, etc.)
2. Ask questions about your project structure, code patterns, or request improvements

For example, you might prompt the LLM with:
- "Analyze this project's structure and suggest improvements"
- "How can I improve the modularization of this project adopting  best practices?"
- "How can I optimize file/function X?"
- "Write numpy-style docstring for all functions from Y"
- "Help me understand the flow of data in this application"
- "Generate comprehensive documentation for this project"

## Next Steps

- Explore [CLI Options](../usage/cli-usage.md) for more advanced usage
- Learn about the [Python API](../usage/python-api.md) for programmatic control
- See [Configuration](../usage/configuration.md) for customizing ProjectLens behavior
- Check out [Use Cases](../guides/use-cases.md) for practical applications
  