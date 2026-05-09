# Pico Bot

A lightweight terminal-based AI assistant for simple, interactive chat.

## Features

-   Terminal chat interface
-   OpenAI integration via LangChain
-   Conversation memory
-   Safe local file access

## Screenshot

![Screenshot](https://raw.githubusercontent.com/ngpeijiun/picobot/master/assets/screenshot.png)

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

## Usage

```bash
picobot
```

Type `exit` or `quit` to leave the session.

## Safety

The `read_file` tool only allows access to files inside the project root directory. This helps prevent path traversal outside the repository.

## Roadmap

-   Add more tools
-   Add tests
-   Improve configuration and error handling

## License

MIT
