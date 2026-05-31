from __future__ import annotations

import shlex
import subprocess
from pathlib import Path

from langchain_core.tools import ToolException, tool

PROJECT_ROOT = Path.cwd().resolve()
TIMEOUT_SECONDS = 10
MAX_OUTPUT_BYTES = 50 * 1024

ALLOWED_COMMANDS = {
    "git status": ["git", "status"],
    "git diff": ["git", "diff"],
    "git diff --cached": ["git", "diff", "--cached"],
    "git log": ["git", "log", "--oneline", "--decorate", "-n", "20"],
    "pytest": ["pytest"],
}

BLOCKED_TOKENS = {";", "&&", "||", "|", ">", "<", "`", "$()"}


def _contains_blocked_tokens(command: str) -> bool:
    return any(token in command for token in BLOCKED_TOKENS)


def _allowed_commands_doc() -> str:
    commands = "\n".join(f"            - {cmd}" for cmd in sorted(ALLOWED_COMMANDS))
    return f"""Run a restricted shell command.

    Args:
        command: One of:
{commands}

    Commands run inside the project root and are limited by timeout.
    """


@tool
def run_shell(command: str) -> str:
    """Run a restricted shell command.

    Args:
        command: One of:
            - git diff
            - git diff --cached
            - git log
            - git status
            - pytest

    Commands run inside the project root and are limited by timeout.
    """

    try:
        command = command.strip()
        if not command:
            raise ToolException("Empty command")
        if _contains_blocked_tokens(command):
            raise ToolException("Blocked shell syntax")

        args = shlex.split(command)
        if not args:
            raise ToolException("Empty command")

        matched_args = None
        for allowed_text, allowed_args in ALLOWED_COMMANDS.items():
            if args == allowed_args:
                matched_args = allowed_args
                break

        if matched_args is None:
            raise ToolException(f"Command not allowed: {command}")

        result = subprocess.run(
            matched_args,
            cwd=PROJECT_ROOT,
            shell=False,
            text=True,
            capture_output=True,
            timeout=TIMEOUT_SECONDS,
            check=False,
        )

        output = (result.stdout or "") + (result.stderr or "")
        data = output.encode("utf-8", errors="replace")
        if len(data) > MAX_OUTPUT_BYTES:
            output = data[:MAX_OUTPUT_BYTES].decode("utf-8", errors="replace") + "\n... (truncated)"

        return f"exit_code={result.returncode}\n{output}".rstrip()

    except subprocess.TimeoutExpired:
        raise ToolException(f"Command timed out after {TIMEOUT_SECONDS}s")
    except ToolException:
        raise
    except Exception as e:
        raise ToolException(str(e)) from e


run_shell.handle_tool_error = True
run_shell.description = _allowed_commands_doc()
