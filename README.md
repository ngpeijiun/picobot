# nano-bot

A lightweight terminal-based AI assistant built for simplicity.

It uses LangChain and OpenAI to support interactive chat.

A safe `read_file` tool provides local, project-only file access.

## Features

-   Simple terminal chat interface
-   Uses OpenAI via LangChain
-   Maintains conversation state with LangGraph memory
-   Safe file-reading tool for project-local files
-   Shows token usage and estimated cost per response

## Example

```terminal
Bot: Hello! Type 'exit' to quit.
You: read README.md
You: hi
Bot: Hi! How can I help?
(input: 130, output: 10, total: 140, cost: $0.0)
You: read README.md
Bot: Read `README.md`. It describes **nano-bot**, a lightweight terminal AI assistant using LangChain/OpenAI, with a safe project-local `read_file` tool, setup/install steps, usage, project structure, safety notes, and roadmap.
(input: 725, output: 70, total: 795, cost: $0.0)
```

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
export OPEN_AI_KEY="your_api_key"
```

On Windows PowerShell:

```powershell
$env:OPEN_AI_KEY="your_api_key"
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
-   Support streaming output
-   Improve configuration and error handling

## License

MIT
