import os

from .delete_path import delete_path
from .edit_file import edit_file
from .list_dir import list_dir
from .move_path import move_path
from .read_file import read_file
from .write_file import write_file

try:
    from langchain_tavily import TavilySearch
except ImportError:
    TavilySearch = None

TOOLS = [
    list_dir,
    read_file,
    write_file,
    edit_file,
    move_path,
    delete_path,
]


def get_tools(enable_web_search: bool = False):
    tools = TOOLS.copy()
    if enable_web_search:
        if TavilySearch is None:
            raise RuntimeError(
                "Tavily support requires the optional dependency. "
                "Install it with: pip install 'picobot[web-search]'"
            )
        if not os.getenv("TAVILY_API_KEY"):
            raise RuntimeError("TAVILY_API_KEY is required to use web search.")
        tools.append(TavilySearch(max_results=5, topic="general"))
    return tools


__all__ = [
    "list_dir",
    "read_file",
    "write_file",
    "edit_file",
    "move_path",
    "delete_path",
    "get_tools",
]
