# Pico Bot

A lightweight terminal-based AI assistant for simple, interactive chat.

## Features

-   Terminal-based chat interface for quick, interactive use
-   OpenAI integration powered by LangChain
-   Conversation memory to preserve context during a session
-   Safe local file access limited to the project root
-   File tools for reading, writing, editing, moving, and deleting within the project root
-   Recursive directory listing support with `config.toml` customization and git-like ignore patterns to reduce noise, token usage, and accidental exposure of unneeded files
-   Accurate cost tracking with cached input token support, down to 6 decimal places

## Usage

```bash
picobot
```

Type `exit` or `quit` to leave the session.

## Reuse as a Library

Other agent developers can import Pico Bot's file tools individually and plug them into their own LangChain agent.

```python
from langchain.agents import create_agent
from picobot.tools import (
    delete_path,
    edit_file,
    list_dir,
    move_path,
    read_file,
    write_file,
)

agent = create_agent(
    model="openai:gpt-5.4-mini",
    tools=[list_dir, read_file, write_file, edit_file, move_path, delete_path],
    system_prompt="Use the file tools carefully.",
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "List the current directory."}]
})
print(result)
```

You can import only the tools your agent needs:

```python
from picobot.tools import read_file, write_file
```

## Screenshot

### File Analysis

![File Analysis](https://raw.githubusercontent.com/ngpeijiun/picobot/master/assets/analysis.png)

### File Editing

![File Editing](https://raw.githubusercontent.com/ngpeijiun/picobot/master/assets/editing.png)

## Installation

### Requirements

-   Python 3.12 (tested)
-   An OpenAI API key

### For Users

Install Pico Bot from PyPI:

```bash
pip install picobot
```

### For Development

Clone the repository and install in editable mode:

```bash
git clone git@github.com:ngpeijiun/picobot.git
cd picobot
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e .
```

## Configuration

Set your OpenAI API key in your environment:

```bash
export OPENAI_API_KEY="your_api_key"
```

On Windows PowerShell:

```powershell
$env:OPENAI_API_KEY="your_api_key"
```

### `config.toml`

You can place a `config.toml` file in your Pico Bot user config directory. Pico Bot reads it from:

On Linux and macOS:

```text
~/.config/picobot/config.toml
```

On Windows:

```text
C:\Users\<YourName>\.config\picobot\config.toml
```

Pico Bot uses this file to configure `list_dir` defaults.

Example:

```toml
[list_dir]
ignore = [".git/", ".venv/", "__pycache__/", "dist/"]
max_depth = 4
max_entries = 500
```

Notes:
- `".venv"` ignores both a file named `.venv` and a directory named `.venv/`
- `".venv/"` ignores only the directory `.venv/`

## Safety

The `read_file` and `list_dir` tools only allow access to files inside the project root directory. This helps prevent path traversal outside the repository.

The `list_dir` tool supports simple gitignore-like ignore patterns to reduce noise, token usage, and accidental exposure of unneeded files. This is intended for convenience only; it is **not** a security boundary and should not be relied on to protect secrets.

## Backward Compatibility

See [Backward Compatibility](https://github.com/ngpeijiun/picobot/blob/master/BACKWARD_COMPATIBILITY.md) for legacy config support. This backward compatibility will be dropped in the official 1.0 release.

## Release Notes

See [Release Notes](RELEASE_NOTES.md) for recent changes and version history.

## Roadmap

-   Add more tools
-   Add tests
-   Improve configuration and error handling

## License

MIT
