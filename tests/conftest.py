# this_file: tests/conftest.py
"""Shared fixtures: a real, minimal TTF built in-memory with fontTools."""

from __future__ import annotations

from pathlib import Path

import pytest
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen


def _make_font(
    path: Path,
    *,
    family: str,
    style: str = "Regular",
    designer: str = "Test Designer",
) -> Path:
    """Build a tiny but valid TTF carrying the given name records.

    It maps the printable ASCII range so the specimen has something to draw.
    """
    glyph_order = [".notdef", "space", *(f"c{cp:04x}" for cp in range(0x21, 0x7F))]
    cmap = {0x20: "space", **{cp: f"c{cp:04x}" for cp in range(0x21, 0x7F)}}

    fb = FontBuilder(unitsPerEm=1000, isTTF=True)
    fb.setupGlyphOrder(glyph_order)
    fb.setupCharacterMap(cmap)

    pen = TTGlyphPen(None)
    pen.moveTo((100, 0))
    pen.lineTo((100, 700))
    pen.lineTo((500, 700))
    pen.lineTo((500, 0))
    pen.closePath()
    box = pen.glyph()
    empty = TTGlyphPen(None).glyph()
    glyphs = {
        name: (empty if name in {".notdef", "space"} else box) for name in glyph_order
    }
    fb.setupGlyf(glyphs)

    fb.setupHorizontalMetrics(dict.fromkeys(glyph_order, (600, 0)))
    fb.setupHorizontalHeader(ascent=800, descent=-200)
    fb.setupNameTable(
        {
            "familyName": family,
            "styleName": style,
            "fullName": f"{family} {style}",
            "psName": f"{family.replace(' ', '')}-{style}",
            "designer": designer,
            "copyright": f"Copyright test {family}",
            "licenseDescription": "Licensed under the Apache License 2.0.",
        }
    )
    fb.setupOS2()
    fb.setupPost()
    fb.font.save(str(path))
    return path


@pytest.fixture
def font_file(tmp_path: Path) -> Path:
    """A single Noto Sans-named font on disk (matches the bundled stub)."""
    return _make_font(tmp_path / "test.ttf", family="Noto Sans")


@pytest.fixture
def make_font(tmp_path: Path):
    """Factory to build extra fonts inside the test's tmp directory."""

    def _factory(name: str, family: str, style: str = "Regular") -> Path:
        return _make_font(tmp_path / name, family=family, style=style)

    return _factory
