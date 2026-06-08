# AGENTS.md
不要读取或修改 tasks.db、app.log、tasks-dashboard.html、task.json
不要大范围重构
优先小步修改
测试命令是 .venv/bin/python -m pytest
## Project rules

This is a Python learning project for a Conso task reward system. Please keep changes small, focused, and easy for a beginner to understand.

## Files that should not be read or modified unless explicitly requested

Do not read, parse, summarize, edit, overwrite, regenerate, or commit the following files unless the user explicitly asks for that specific file:

* `tasks.db`
* `app.log`
* `tasks-dashboard.html`
* `task.json`
* `.venv/`
* `__pycache__/`
* `.DS_Store`

## SQLite migration rules

The project is migrating from JSON storage to SQLite storage.

Current direction:

* Write operations should use SQLite functions in `storage.py`.
* Keep `tasks_data` as the in-memory working list during the transition.
* When a write operation changes the database, also update `tasks_data` so the current running session stays in sync.
* Do not reintroduce `task.json` as the main storage source.

## Preferred edit scope

Before editing, identify the exact files and functions that need changes.

Prefer modifying only the necessary files.

Avoid broad refactors unless explicitly requested.

Do not modify unrelated files.

## Test command

After code changes, run:

```bash
.venv/bin/python -m pytest
```

If manual testing is needed, run:

```bash
.venv/bin/python taskgane-v1.py
```
