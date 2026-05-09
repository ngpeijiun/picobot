# nano-bot

A lightweight terminal-based AI assistant built for simplicity.

It uses LangChain and OpenAI to support interactive chat.

A safe `read_file` tool provides local, project-only file access.

## Features

-   Simple terminal chat interface
-   Uses OpenAI models via LangChain
-   Maintains conversation state with LangGraph memory
-   Safe file-reading tool for project-local files
-   Displays tool calls and tool results in the terminal for transparency
-   Shows token usage and estimated cost per response

## Example

![Screenshot](https://raw.githubusercontent.com/ngpeijiun/nano-bot/master/assets/screenshot.png)

## Installation

### Requirements

-   Python 3.12 (tested)
-   An OpenAI API key

### Setup

```bash
git clone git@github.com:ngpeijiun/nano-bot.git
cd nano-bot
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
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
python nano.py
```

Type `exit` or `quit` to leave the session.

## Project Structure

-   `nano.py` - CLI chat application
-   `read_file.py` - safe file-reading tool
-   `requirements.txt` - Python dependencies
-   `README.md` - project documentation

## Safety

The `read_file` tool only allows access to files inside the project root directory. This helps prevent path traversal outside the repository.

## Roadmap

-   Add more tools
-   Add tests
-   Improve configuration and error handling

## License

MIT
