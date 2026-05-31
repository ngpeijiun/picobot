from langchain_core.tools import ToolException, tool

from .path_utils import resolve_project_path


@tool
def move_path(src: str, dst: str) -> str:
    """Move or rename a file or directory.

    Args:
        src: A source path.
        dst: A destination path.
    """
    try:
        src_path = resolve_project_path(src)
        dst_path = resolve_project_path(dst)

        if dst_path.exists():
            raise ToolException(f"Destination already exists: {dst}")

        dst_path.parent.mkdir(parents=True, exist_ok=True)
        src_path.rename(dst_path)

        return f"Moved {src} -> {dst}"

    except FileNotFoundError:
        raise ToolException(f"Path not found: {src}")
    except FileExistsError:
        raise ToolException(f"Destination already exists: {dst}")
    except PermissionError:
        raise ToolException(f"Permission denied: {src}")
    except ToolException:
        raise
    except Exception as e:
        raise ToolException(str(e)) from e

move_path.handle_tool_error = True
