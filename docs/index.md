# ProjectLens

<div class="grid cards" markdown>

-   :mag: __Project Scanning Made Simple__

    ---

    Export your project files with smart filtering for LLM analysis and beyond.

    [:arrow_right: Getting started](getting-started/quick-start.md)

-   :package: __Zero Dependencies__

    ---

    Built with pure Python - no external packages required.

    [:arrow_right: Installation](getting-started/installation.md)

-   :rocket: __CLI & API Support__

    ---

    Use as a command-line tool or integrate with your Python scripts.
    
    [:arrow_right: CLI usage](usage/cli-usage.md)  
    [:arrow_right: Python API](usage/python-api.md)

-   :evergreen_tree: __Intelligent Filtering__

    ---

    Focus on the files that matter - filter by extension, size, and pattern.

    [:arrow_right: Configuration](usage/configuration.md)

</div>


## What is ProjectLens?

ProjectLens is a specialized tool for developers and teams who want to leverage LLMs (Large Language Models) like ChatGPT, Claude, and DeepSeek for code analysis, documentation generation, and codebase understanding.

It creates a comprehensive, well-formatted snapshot of your project that:

1. **Respects common ignore patterns** (automatically skips venv, cache, build directories)
2. **Filters by file extension** (focus on just your code, not binaries or generated files)
3. **Manages context limits** (skip files that are too large)
4. **Creates structured output** with tree visualization and clear file boundaries

## Why Use ProjectLens?

When working with AI assistants on code projects, you often need to provide context about your codebase. Manually collecting and formatting this information is tedious and error-prone.

ProjectLens solves this by:

- **Automating the collection process** - scan an entire project with a single command
- **Creating consistent, well-formatted output** optimized for AI consumption
- **Preserving project structure** through tree visualization
- **Respecting sensitive content** through intelligent filtering

## Key Features

- 🔍 Recursively collect project files with specified extensions and smart filtering
- 🌲 Generate detailed project tree structure 
- 📝 Create well-formatted output optimized for LLM analysis
- 🚀 Easy to use as both CLI tool and Python API
- 🛠️ Zero external dependencies

## License

ProjectLens is released under the [MIT License](https://github.com/cmcouto-silva/projectlens/blob/main/LICENSE).

## Creator

ProjectLens is created and maintained by [Cainã Max Couto da Silva](https://github.com/cmcouto-silva).

## Donate

Like it? Consider [buying me a coffee](buymeacoffee.com/cmcoutosilva) (don't forget the message) 😊