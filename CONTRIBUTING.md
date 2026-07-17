# Contributing

1. Fork the repository and create a focused branch.
2. Install dependencies with `pip install -r requirements-dev.txt`.
3. Run `python -m pytest -q`.
4. Run `python -m py_compile TimePulse.py`.
5. Keep pull requests focused and document behavior changes.
6. Do not commit personal alarm data, logs, build output, credentials, or generated executables.

Bug reports should include Windows version, TimePulse version, reproduction steps, expected behavior, actual behavior, and relevant entries from `%LOCALAPPDATA%\TimePulse\TimePulse.log`.
