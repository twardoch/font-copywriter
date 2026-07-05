# this_file: tests/test_copywriter.py
"""Tests for font_copywriter: metadata round-trip, rendering, and file output."""

from __future__ import annotations

from pathlib import Path

import pytest

from font_copywriter import (
    FontMetadata,
    copywrite,
    default_stub_folder,
    read_metadata,
    render_description,
    render_specimen,
)


def test_read_metadata_round_trip(font_file: Path) -> None:
    """What conftest wrote into the name table is what we read back."""
    meta = read_metadata(font_file)
    assert meta.family == "Noto Sans"
    assert meta.subfamily == "Regular"
    assert meta.full_name == "Noto Sans Regular"
    assert meta.designer == "Test Designer"
    assert "Apache" in meta.license
    assert meta.glyph_count > 0
    assert 0x41 in meta.characters  # "A" was mapped


def test_read_metadata_missing_fields_are_empty(make_font) -> None:
    """A font we did read still yields strings, never None, for absent records."""
    path = make_font("plain.ttf", family="Bare Family")
    meta = read_metadata(path)
    assert meta.family == "Bare Family"
    assert isinstance(meta.designer, str)


def test_slug_strips_whitespace() -> None:
    meta = FontMetadata("Noto Sans", "", "", "", "", "", 0, ())
    assert meta.slug == "NotoSans"


def test_slug_falls_back_when_family_blank() -> None:
    meta = FontMetadata("", "", "", "", "", "", 0, ())
    assert meta.slug == "font"


def test_render_description_uses_stub() -> None:
    meta = FontMetadata(
        "Noto Sans", "Regular", "Noto Sans Regular", "", "", "", 42, (65,)
    )
    out = render_description(meta, stub="A stub blurb.")
    assert out.startswith("# Noto Sans")
    assert "A stub blurb." in out
    assert "**Glyphs:** 42" in out


def test_render_description_without_stub_still_has_facts() -> None:
    meta = FontMetadata("Bare", "Bold", "Bare Bold", "", "", "", 3, (65, 66))
    out = render_description(meta)
    assert "# Bare" in out
    assert "**Characters:** 2" in out


def test_render_specimen_keeps_only_drawable_chars() -> None:
    # Only "A" (0x41) and space are mapped; the rest of the pangram is dropped.
    meta = FontMetadata("Bare", "", "Bare Regular", "", "", "", 2, (0x41,))
    out = render_specimen(meta)
    assert out.startswith("Bare Regular")
    body = out.splitlines()[-1]
    assert set(body) <= {"A", " "}


def test_copywrite_single_font_writes_description(
    font_file: Path, tmp_path: Path
) -> None:
    desc = tmp_path / "desc"
    written = copywrite(font_file, desc)
    assert len(written) == 1
    text = written[0].read_text(encoding="utf-8")
    assert written[0].name == "NotoSans.md"
    # The bundled Noto Sans stub was matched and injected.
    assert "sans serif" in text.lower()


def test_copywrite_writes_art_when_requested(font_file: Path, tmp_path: Path) -> None:
    desc, art = tmp_path / "desc", tmp_path / "art"
    copywrite(font_file, desc, art_path=art)
    specimen = art / "NotoSans.txt"
    assert specimen.is_file()
    assert "Noto Sans" in specimen.read_text(encoding="utf-8")


def test_copywrite_folder_processes_every_font(make_font, tmp_path: Path) -> None:
    make_font("a.ttf", family="Alpha Sans")
    make_font("b.ttf", family="Beta Serif")
    src = (tmp_path / "a.ttf").parent
    desc = tmp_path / "out"
    written = copywrite(src, desc)
    names = {p.name for p in written}
    assert {"AlphaSans.md", "BetaSerif.md"} <= names


def test_copywrite_empty_source_raises(tmp_path: Path) -> None:
    empty = tmp_path / "empty"
    empty.mkdir()
    with pytest.raises(FileNotFoundError):
        copywrite(empty, tmp_path / "desc")


def test_default_stub_folder_is_bundled() -> None:
    folder = default_stub_folder()
    assert folder.is_dir()
    assert (folder / "NotoSans.md").is_file()
