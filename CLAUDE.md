# CLAUDE.md

See [AGENTS.md](AGENTS.md) for the full guide to working in this repo. In short:

- The tool is `src/font_copywriter/copywriter.py`; the rest is scaffolding.
- `uv venv && uv pip install -e ".[dev,test]"` to set up.
- Before claiming done: `uv run ruff check . && uv run mypy src/font_copywriter && uv run pytest`.
- Keep functions total and honest; follow the STYLE_GUIDE for all prose.
- Release with `uvx gitnextver@latest .` (PyPI publishing stays off for now).
