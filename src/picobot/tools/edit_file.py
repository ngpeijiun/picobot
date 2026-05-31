from langchain_core.tools import ToolException, tool

from .path_utils import resolve_project_path

MAX_FILE_SIZE = 50 * 1024  # 50 KB


@tool
def edit_file(path: str, old_text: str, new_text: str) -> str:
    """Edit a text file by replacing an exact text block.

    Args:
        path: A file path to edit.
        old_text: Exact text to replace.
        new_text: Replacement text.
    """

    try:
        full_path = resolve_project_path(path)

        content = full_path.read_text(encoding="utf-8")

        if old_text not in content:
            raise ToolException(f"Text not found in file: {path}")
        if content.count(old_text) > 1:
            raise ToolException(f"Text appears multiple times in file: {path}")

        updated = content.replace(old_text, new_text, 1)

        if len(updated.encode("utf-8")) > MAX_FILE_SIZE:
            raise ToolException(f"Updated content too large (>50KB): {path}")

        full_path.write_text(updated, encoding="utf-8")

        return f"Edited {path}"

    except FileNotFoundError:
        raise ToolException(f"File not found: {path}")
    except IsADirectoryError:
        raise ToolException(f"Is a directory: {path}")
    except PermissionError:
        raise ToolException(f"Permission denied: {path}")
    except UnicodeDecodeError:
        raise ToolException(f"Could not decode file as text: {path}")
    except UnicodeEncodeError:
        raise ToolException("Could not encode the new content")
    except ToolException:
        raise
    except Exception as e:
        raise ToolException(str(e)) from e

edit_file.handle_tool_error = True
