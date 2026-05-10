from langchain_core.tools import ToolException, tool

from .path_utils import resolve_project_path

MAX_DIR_ENTRIES = 500


@tool
def list_dir(path: str = "/") -> str:
    """list dir"""

    try:
        full_path = resolve_project_path(path)
        entries = sorted(full_path.iterdir(), key=lambda x: (not x.is_dir(), x.name))

        items = []
        truncated = len(entries) > MAX_DIR_ENTRIES
        for p in entries[:MAX_DIR_ENTRIES]:
            suffix = "/" if p.is_dir() else ""
            items.append(p.name + suffix)

        if truncated:
            items.append(f"... ({len(entries) - MAX_DIR_ENTRIES} more entries)")

        return "\n".join(items) if items else "(empty)"

    except FileNotFoundError:
        raise ToolException(f"Path not found: {path}")
    except NotADirectoryError:
        raise ToolException(f"Is not a directory: {path}")
    except PermissionError:
        raise ToolException(f"Permission denied: {path}")
    except ToolException:
        raise
    except Exception as e:
        raise ToolException(str(e)) from e

list_dir.handle_tool_error = True
