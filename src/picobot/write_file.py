from langchain_core.tools import ToolException, tool

from .path_utils import resolve_project_path

MAX_FILE_SIZE = 50 * 1024  # 50 KB


@tool
def write_file(path: str, content: str) -> str:
    """Write text to a file.

    Automatically creates parent directories if they do not exist.

    Args:
        path: A file path to write.
        content: Text content to write.
    """

    try:
        full_path = resolve_project_path(path)

        if len(content.encode("utf-8")) > MAX_FILE_SIZE:
            raise ToolException(f"Content too large (>50KB): {path}")

        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content, encoding="utf-8")

        return f"Wrote {len(content.encode('utf-8'))} bytes to {path}"

    except IsADirectoryError:
        raise ToolException(f"Is a directory: {path}")
    except PermissionError:
        raise ToolException(f"Permission denied: {path}")
    except UnicodeEncodeError:
        raise ToolException("Could not encode the content")
    except ToolException:
        raise
    except Exception as e:
        raise ToolException(str(e)) from e

write_file.handle_tool_error = True
