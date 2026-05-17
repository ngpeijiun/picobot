# Backward Compatibility

## Configuration section names

`config.toml` now prefers the `[list_dir]` section for `list_dir` defaults.

For backward compatibility, `[tree]` is still supported and treated the same as `[list_dir]`.

### Example

Preferred:

```toml
[list_dir]
ignore = [".git", ".venv", "__pycache__", "dist"]
max_depth = 4
max_entries = 500
```

Legacy supported form:

```toml
[tree]
ignore = [".git", ".venv", "__pycache__", "dist"]
max_depth = 4
max_entries = 500
```
