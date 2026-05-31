from langchain_core.tools import ToolException, tool

from ..config import CONFIG
from .path_utils import display_path, is_ignored_path, resolve_project_path


@tool
def list_dir(path: str = ".", depth: int = 0) -> str:
    """List a directory as a tree.

    Args:
        path: Directory path to list.
        depth: Recursion depth. 0 shows only immediate entries.
    """

    try:
        if depth < 0:
            raise ToolException("depth must be >= 0")

        depth = min(depth, CONFIG.list_dir.max_depth)
        max_entries = CONFIG.list_dir.max_entries
        full_path = resolve_project_path(path)

        if not full_path.exists():
            raise ToolException(f"Path not found: {path}")
        if not full_path.is_dir():
            raise ToolException(f"Is not a directory: {path}")

        lines = []
        count = 0

        def walk(p, prefix="", remaining=depth):
            nonlocal count
            if count >= max_entries:
                return

            entries = sorted(
                (x for x in p.iterdir() if not is_ignored_path(x)),
                key=lambda x: (not x.is_dir(), x.name),
            )
            for i, child in enumerate(entries):
                if count >= max_entries:
                    return

                is_last = i == len(entries) - 1
                branch = "└── " if is_last else "├── "
                suffix = "/" if child.is_dir() else ""
                lines.append(f"{prefix}{branch}{child.name}{suffix}")
                count += 1

                if child.is_dir() and remaining > 0:
                    extension = "    " if is_last else "│   "
                    walk(child, prefix + extension, remaining - 1)

        lines.append(display_path(full_path))
        walk(full_path)

        if count >= max_entries:
            lines.append(f"... (truncated at {max_entries} entries)")

        return "\n".join(lines)

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
