from pathlib import Path

from langchain_core.tools import ToolException

from .config import CONFIG

PROJECT_ROOT = Path.cwd().resolve()


def resolve_project_path(path: str) -> Path:
    """Resolve a user-provided path against the project root.

    The returned path is guaranteed to stay within the project root.

    Args:
        path: A relative path provided by the user.

    Returns:
        The resolved absolute path within the project root.

    Raises:
        ToolException: If the resolved path would escape the project root.
    """

    full_path = (PROJECT_ROOT / path).resolve()
    if not full_path.is_relative_to(PROJECT_ROOT):
        raise ToolException(f"Path outside project root: {path}")
    return full_path


def display_path(full_path: Path) -> str:
    """Format a path for display relative to the project root.

    The input path must already be guaranteed to be within project root,
    for example by first calling resolve_project_path().

    Args:
        full_path: An absolute path within the project root.

    Returns:
        The path shown relative to project root, with a trailing slash added
        for directories.
    """

    rel = full_path.resolve().relative_to(PROJECT_ROOT)
    return f"{rel}/" if full_path.is_dir() else str(rel)


def is_ignored_path(child: Path, ignore: list[str] | None = None) -> bool:
    """Determine whether a path should be ignored.

    The ignore rules follow simple gitignore-like directory matching.

    Args:
        child: The path to check.
        ignore: Optional custom ignore list. Uses the configured list_dir ignore
            list when omitted.

    Returns:
        True if the path matches an ignore rule, otherwise False.
    """

    ignore_list = CONFIG.list_dir.ignore if ignore is None else ignore
    return any(
        ignore_item == child.name
        or (
            ignore_item.endswith("/")
            and child.is_dir()
            and child.name == ignore_item[:-1]
        )
        for ignore_item in ignore_list
    )
