from langchain_core.tools import ToolException, tool

from .path_utils import resolve_project_path


@tool
def delete_path(path: str, is_dir: bool = False) -> str:
    """Delete a file or directory.

    Args:
        path: A file or directory path to delete.
        is_dir: Set True to delete a directory.
    """
    try:
        full_path = resolve_project_path(path)

        if full_path.is_dir():
            if not is_dir:
                raise ToolException(f"Is a directory: {path} (set is_dir=True to delete)")
            full_path.rmdir()
        else:
            if is_dir:
                raise ToolException(f"Not a directory: {path}")
            full_path.unlink()

        return f"Deleted {path}"

    except FileNotFoundError:
        raise ToolException(f"Path not found: {path}")
    except PermissionError:
        raise ToolException(f"Permission denied: {path}")
    except ToolException:
        raise
    except Exception as e:
        raise ToolException(str(e)) from e

delete_path.handle_tool_error = True
