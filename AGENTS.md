# AGENTS.md

Guidance for AI agents (and humans) working in this repo.

## What this is

`font-copywriter` reads a font's `name` and `cmap` tables with fontTools and
writes a Markdown description plus an optional plain-text specimen. The whole
tool is `src/font_copywriter/copywriter.py`; everything else is scaffolding.

## Layout

- `src/font_copywriter/copywriter.py` — the tool: `read_metadata`, `copywrite`,
  and the render helpers.
- `src/font_copywriter/__main__.py` — the `font-copywriter` CLI (python-fire).
- `src/font_copywriter/data/stubs/` — bundled per-family Markdown blurbs.
- `tests/` — pytest suite; `conftest.py` builds a real TTF in memory with
  `fontTools.fontBuilder`, so tests need no binary fixtures on disk.
- `docs/` — Jekyll + Just-the-Docs site.

## Working here

- Python ≥ 3.10, `src/` layout, hatch-vcs versioning (tags drive the version).
- Set up: `uv venv && uv pip install -e ".[dev,test]"`.
- Before you claim done, all three must pass:
  ```bash
  uv run ruff check . && uv run ruff format --check .
  uv run mypy src/font_copywriter
  uv run pytest
  ```
- Keep it total and honest: missing `name` records read back as `""`, never
  `None`; an empty font source raises `FileNotFoundError` rather than writing
  nothing and calling it success.
- Prose (README, docs, stubs, comments) follows the repo STYLE_GUIDE: hook fast,
  cut jargon, show don't gesture.

## Release

`uvx gitnextver@latest .` commits, tags the next `vX.Y.Z`, and pushes. The
`release.yml` workflow then builds and cuts a GitHub release. PyPI publishing is
intentionally off until the descriptions are judged good enough.
