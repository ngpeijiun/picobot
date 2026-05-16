from langchain_core.tools import ToolException, tool

from .path_utils import resolve_project_path

MAX_FILE_SIZE = 50 * 1024  # 50 KB


@tool
def read_file(path: str) -> str:
    """Read a text file.

    Args:
        path: A file path to read.
    """

    try:
        full_path = resolve_project_path(path)

        if full_path.stat().st_size > MAX_FILE_SIZE:
            raise ToolException(f"File too large (>50KB): {path}")

        return full_path.read_text(encoding="utf-8")

    except FileNotFoundError:
        raise ToolException(f"File not found: {path}")
    except IsADirectoryError:
        raise ToolException(f"Is a directory: {path}")
    except PermissionError:
        raise ToolException(f"Permission denied: {path}")
    except UnicodeDecodeError:
        raise ToolException(f"Could not decode file as text: {path}")
    except ToolException:
        raise
    except Exception as e:
        raise ToolException(str(e)) from e

read_file.handle_tool_error = True
