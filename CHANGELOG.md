# Changelog

All notable changes to `font-copywriter` are recorded here.

## [Unreleased]

### Added

- **Implemented the core `copywrite()` function.** It was a `pass` stub; it now
  reads a font with fontTools and writes a Markdown description plus an optional
  character specimen, for one font or a whole folder.
- `read_metadata()` returning a frozen `FontMetadata` (family, subfamily, full
  name, designer, copyright, licence, glyph count, mapped codepoints).
- `render_description()`, `render_specimen()`, and `default_stub_folder()` as
  part of the public API.
- Stub matching by folded family name, with the bundled Noto stubs used by
  default when no stub folder is given.
- `src/font_copywriter/data/stubs/README.md` documenting the stub format.
- Test suite (12 tests) built on an in-memory fontTools fixture, covering the
  metadata round-trip, rendering, folder processing, and the empty-source error.
- GitHub Actions: `ci.yml` (ruff, mypy, pytest on Linux/macOS × Python
  3.10–3.12) and `release.yml` (build and GitHub release on tag).
- Jekyll + Just-the-Docs documentation under `docs/`, with a generated icon.

### Changed

- Migrated packaging from `setup.py` to `pyproject.toml` with hatchling and
  hatch-vcs (version derived from git tags).
- Moved the package to a `src/` layout (`src/font_copywriter/`).
- Rewrote `README.md` to describe the working tool rather than the planned one.
- Added `fontTools` and `fire` as declared dependencies.

### Removed

- `setup.py` and the empty `requirements.txt`.
- Tracked `.DS_Store` (now git-ignored).
