from pathlib import Path

from langchain_core.tools import ToolException, tool

@tool
def read_file(path: str) -> str:
    """read file"""

    try:
        base_dir = Path.cwd()
        clean_path = Path(path).as_posix().lstrip("/")
        full_path = (base_dir / clean_path).resolve()

        if not full_path.is_relative_to(base_dir):
            raise ValueError(f"Path outside project root: {path}")

        with open(full_path, "r") as f:
            return f.read()
    except Exception as e:
        raise ToolException(str(e)) from e

read_file.handle_tool_error = True
