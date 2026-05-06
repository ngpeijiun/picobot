from pathlib import Path

from langchain_core.tools import ToolException, tool

MAX_FILE_SIZE = 50 * 1024  # 50 KB


@tool
def read_file(path: str) -> str:
    """read file"""

    try:
        base_dir = Path.cwd()
        clean_path = Path(path).as_posix().lstrip("/")
        full_path = (base_dir / clean_path).resolve()

        if not full_path.is_relative_to(base_dir):
            raise ToolException(f"Path outside project root: {path}")

        if full_path.stat().st_size > MAX_FILE_SIZE:
            raise ToolException(f"File too large (>50KB): {path}")

        with open(full_path, "r") as f:
            return f.read()
    except FileNotFoundError:
        raise ToolException(f"File not found: {path}")
    except IsADirectoryError:
        raise ToolException(f"Is a directory: {path}")
    except PermissionError:
        raise ToolException(f"Permission denied: {path}")
    except UnicodeDecodeError:
        raise ToolException(f"Could not decode file as text: {path}")
    except ToolException as e:
        raise ToolException(str(e))
    except Exception as e:
        raise ToolException(str(e)) from e

read_file.handle_tool_error = True
