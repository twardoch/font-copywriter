#!/usr/bin/env python3
# this_file: src/font_copywriter/copywriter.py
"""Turn a font into words.

`font-copywriter` reads a font's ``name`` and ``cmap`` tables with fontTools,
pairs the family with a hand-written Markdown *stub* (a blurb such as
``data/stubs/NotoSans.md``), and writes two files: a description and a small
character specimen. Point it at one font or a whole folder.
"""

from __future__ import annotations

from dataclasses import dataclass
from importlib import resources
from pathlib import Path

from fontTools.ttLib import TTFont

# OpenType `name` table IDs. The full list lives in the spec:
# https://learn.microsoft.com/typography/opentype/spec/name#name-ids
_COPYRIGHT = 0
_FAMILY = 1
_SUBFAMILY = 2
_FULL_NAME = 4
_DESIGNER = 9
_LICENSE = 13
_TYPO_FAMILY = 16

# Suffixes we treat as fonts when scanning a folder.
_FONT_SUFFIXES = {".ttf", ".otf", ".ttc", ".otc"}

# A stock line to probe what the font can actually draw. Only the glyphs the
# font maps survive into the specimen.
_SPECIMEN_SAMPLE = "The quick brown fox jumps over the lazy dog 0123456789"


@dataclass(frozen=True)
class FontMetadata:
    """The handful of `name`/`cmap` facts a description is built from.

    Every field is populated at read time, so a `FontMetadata` that exists is a
    font that parsed. Missing name records become empty strings, never `None` —
    the caller never has to guard.
    """

    family: str
    subfamily: str
    full_name: str
    designer: str
    copyright: str
    license: str
    glyph_count: int
    characters: tuple[int, ...]  # sorted Unicode codepoints present in the cmap

    @property
    def slug(self) -> str:
        """Family name with whitespace stripped: ``Noto Sans`` -> ``NotoSans``.

        Used for output filenames and to match stub files.
        """
        return "".join(self.family.split()) or "font"


def _read_name(font: TTFont, name_id: int) -> str:
    """Return one `name` record as text, or ``""`` when the font omits it."""
    name_table = font.get("name")
    if name_table is None:
        return ""
    return name_table.getDebugName(name_id) or ""


def read_metadata(font_path: Path | str, font_number: int = 0) -> FontMetadata:
    """Read the descriptive metadata out of a single font file.

    `font_number` selects a face inside a ``.ttc``/``.otc`` collection. The font
    is always closed before returning, even if a table is malformed.
    """
    font = TTFont(font_path, fontNumber=font_number, lazy=True)
    try:
        cmap = font.getBestCmap() if "cmap" in font else {}
        family = _read_name(font, _TYPO_FAMILY) or _read_name(font, _FAMILY)
        return FontMetadata(
            family=family,
            subfamily=_read_name(font, _SUBFAMILY),
            full_name=_read_name(font, _FULL_NAME),
            designer=_read_name(font, _DESIGNER),
            copyright=_read_name(font, _COPYRIGHT),
            license=_read_name(font, _LICENSE),
            glyph_count=len(font.getGlyphOrder()),
            characters=tuple(sorted(cmap)),
        )
    finally:
        font.close()


def default_stub_folder() -> Path:
    """Path to the Noto stubs shipped inside the package."""
    return Path(str(resources.files("font_copywriter") / "data" / "stubs"))


def _normalize(text: str) -> str:
    """Fold a name to lowercase alphanumerics so ``Noto Sans`` == ``NotoSans``."""
    return "".join(ch for ch in text.lower() if ch.isalnum())


def _find_stub(meta: FontMetadata, stub_folder: Path | None) -> str:
    """Return the text of the stub matching this family, or ``""`` if none fits."""
    if stub_folder is None or not stub_folder.is_dir():
        return ""
    key = _normalize(meta.family)
    for stub in sorted(stub_folder.glob("*.md")):
        if _normalize(stub.stem) == key:
            return stub.read_text(encoding="utf-8").strip()
    return ""


def render_description(meta: FontMetadata, stub: str = "") -> str:
    """Compose the Markdown description for one font.

    The stub, when present, carries the voice; the metadata carries the facts.
    """
    lines = [f"# {meta.family}", ""]
    if stub:
        lines += [stub, ""]
    lines.append(f"- **Styles:** {meta.subfamily or '—'}")
    lines.append(f"- **Glyphs:** {meta.glyph_count}")
    lines.append(f"- **Characters:** {len(meta.characters)}")
    if meta.designer:
        lines.append(f"- **Designer:** {meta.designer}")
    if meta.license:
        lines += ["", "## License", "", meta.license]
    return "\n".join(lines).rstrip() + "\n"


def render_specimen(meta: FontMetadata) -> str:
    """Compose a plain-text specimen: the font's name over what it can draw."""
    drawable = set(meta.characters)
    sample = "".join(ch for ch in _SPECIMEN_SAMPLE if ch == " " or ord(ch) in drawable)
    return f"{meta.full_name or meta.family}\n\n{sample}\n"


def _collect_fonts(source: Path) -> list[Path]:
    """List the font files at `source`, whether it is one file or a folder."""
    if source.is_file():
        return [source]
    if source.is_dir():
        return sorted(p for p in source.iterdir() if p.suffix.lower() in _FONT_SUFFIXES)
    return []


def copywrite(
    font_path_or_folder: Path | str,
    desc_path: Path | str,
    art_path: Path | str | None = None,
    stub_folder: Path | str | None = None,
) -> list[Path]:
    """Describe one font, or every font in a folder.

    For each font this writes ``<desc_path>/<Family>.md`` (the description) and,
    when `art_path` is given, ``<art_path>/<Family>.txt`` (the specimen). When
    `stub_folder` is omitted the bundled Noto stubs are used. Returns the list
    of description files written.

    Raises `FileNotFoundError` when `font_path_or_folder` holds no fonts, so a
    silent empty run can't be mistaken for success.
    """
    source = Path(font_path_or_folder)
    fonts = _collect_fonts(source)
    if not fonts:
        msg = f"No font files found at {source}"
        raise FileNotFoundError(msg)

    desc_dir = Path(desc_path)
    desc_dir.mkdir(parents=True, exist_ok=True)
    art_dir = Path(art_path) if art_path is not None else None
    if art_dir is not None:
        art_dir.mkdir(parents=True, exist_ok=True)
    stubs = Path(stub_folder) if stub_folder is not None else default_stub_folder()

    written: list[Path] = []
    for font_file in fonts:
        meta = read_metadata(font_file)
        name = meta.slug or font_file.stem
        desc_file = desc_dir / f"{name}.md"
        desc_file.write_text(
            render_description(meta, _find_stub(meta, stubs)), encoding="utf-8"
        )
        written.append(desc_file)
        if art_dir is not None:
            (art_dir / f"{name}.txt").write_text(
                render_specimen(meta), encoding="utf-8"
            )
    return written
