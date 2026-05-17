from dataclasses import dataclass, field
from pathlib import Path
import tomllib

from platformdirs import user_config_dir

CONFIG_PATH = Path(user_config_dir("picobot")) / "config.toml"

DEFAULT_IGNORE = [".git", ".venv", "__pycache__"]


class ConfigError(Exception):
    pass


@dataclass
class ListDirConfig:
    ignore: list[str] = field(default_factory=lambda: DEFAULT_IGNORE.copy())
    max_depth: int = 4
    max_entries: int = 500


@dataclass
class AppConfig:
    list_dir: ListDirConfig = field(default_factory=ListDirConfig)


def load_config() -> AppConfig:
    cfg = AppConfig()

    if not CONFIG_PATH.exists():
        return cfg

    try:
        with open(CONFIG_PATH, "rb") as f:
            data = tomllib.load(f)
    except OSError as e:
        raise ConfigError(f"Failed to read config file {CONFIG_PATH}: {e}") from e
    except tomllib.TOMLDecodeError as e:
        raise ConfigError(f"Invalid TOML in config file {CONFIG_PATH}: {e}") from e

    list_dir_data = data.get("list_dir", data.get("tree", {}))
    if not isinstance(list_dir_data, dict):
        raise ConfigError("[list_dir] section must be a table")

    ignore = list_dir_data.get("ignore", cfg.list_dir.ignore)
    if not isinstance(ignore, list) or not all(isinstance(x, str) for x in ignore):
        raise ConfigError("[list_dir.ignore] must be a list of strings")
    cfg.list_dir.ignore = list(ignore)

    max_depth = list_dir_data.get("max_depth", cfg.list_dir.max_depth)
    if not isinstance(max_depth, int) or isinstance(max_depth, bool):
        raise ConfigError("[list_dir.max_depth] must be an integer")
    cfg.list_dir.max_depth = max_depth

    max_entries = list_dir_data.get("max_entries", cfg.list_dir.max_entries)
    if not isinstance(max_entries, int) or isinstance(max_entries, bool):
        raise ConfigError("[list_dir.max_entries] must be an integer")
    cfg.list_dir.max_entries = max_entries

    return cfg

CONFIG = load_config()
