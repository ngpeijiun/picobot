from pathlib import Path

from langchain_core.tools import ToolException


def resolve_project_path(path: str) -> Path:
    base_dir = Path.cwd()
    clean_path = Path(path.replace("\\", "/")).as_posix().lstrip("/")
    full_path = (base_dir / clean_path).resolve()

    if not full_path.is_relative_to(base_dir):
        raise ToolException(f"Path outside project root: {path}")

    return full_path
