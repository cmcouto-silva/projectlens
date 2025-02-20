# Installation

ProjectLens is designed to be lightweight with zero external dependencies, making installation quick and straightforward.

## Prerequisites

- Python 3.9 or higher

## Installing from PyPI

The recommended installation method is via pip:

```bash
pip install projectlens
```

This will install the latest stable version of ProjectLens from PyPI.

## Development Installation

If you want to contribute to ProjectLens or use the latest development version, you can install directly from the repository:

```bash
git clone https://github.com/cmcouto-silva/projectlens
cd projectlens
```

I recommend using [UV](https://github.com/astral-sh/uv):

```bash
# Using pip
pip install -e .

# Using uv (faster)
uv sync
```

## Verifying Installation

To verify that ProjectLens was installed correctly, run:

```bash
projectlens --help
```

You should see the help output displaying available commands and options.

## Installation in Virtual Environments

It's generally a good practice to install Python packages in a virtual environment. UV installs it for you.

```bash
# Create the virtual environment & install projectlens
uv sync

# Activate the environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate
```

This package uses only built-in Python functions: 0 dependencies!


## Next Steps

- [Quick Start Guide](quick-start.md) - Learn how to use ProjectLens
- [CLI Usage](../usage/cli-usage.md) - Explore command-line options
- [Python API](../usage/python-api.md) - Use ProjectLens in your Python scripts