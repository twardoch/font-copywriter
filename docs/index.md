---
layout: home
title: font-copywriter
---

# font-copywriter

Point it at a font. Get back a paragraph a human can read.

`font-copywriter` opens a font with [fontTools](https://github.com/fonttools/fonttools), pulls the family name, styles, glyph and character counts, designer, and licence out of the `name` and `cmap` tables, and writes a Markdown description. If a matching *stub* — a hand-written blurb for that family — is on hand, it goes in at the top, so the prose carries voice while the numbers carry proof.

![font-copywriter](assets/icon.png){: style="max-width:320px"}

## Install

Not on PyPI yet. Install from source:

```bash
pip install git+https://github.com/twardoch/font-copywriter
```

## Quick start

```bash
# One font -> descriptions/NotoSans.md
font-copywriter NotoSans-Regular.ttf descriptions/

# Also write a plain-text specimen into art/
font-copywriter NotoSans-Regular.ttf descriptions/ art/

# A whole folder of fonts, using your own stubs instead of the bundled Noto set
font-copywriter fonts/ descriptions/ art/ my-stubs/
```

Omit the stub folder to fall back on the Noto stubs shipped inside the package.

## In Python

```python
from font_copywriter import copywrite, read_metadata

# Just the facts
meta = read_metadata("NotoSans-Regular.ttf")
print(meta.family, meta.glyph_count)

# Write description (+ specimen) files, return the paths written
written = copywrite("fonts/", "descriptions/", art_path="art/")
```

## How it works

1. **Read** — fontTools opens each font; the `name` table gives family, styles, designer, and licence, the `cmap` gives the character set. Missing records come back as empty strings, never `None`.
2. **Match** — the family name is folded to lowercase letters and digits (`Noto Sans` → `notosans`) and matched against the stub filenames (`NotoSans.md`). A hit supplies the blurb; a miss just skips it.
3. **Write** — a Markdown description lands in the description folder as `<Family>.md`; when an art folder is given, a text specimen lands there as `<Family>.txt`, holding only the characters the font can actually draw.

## Stubs

A stub is one Markdown file per family, named after the family with spaces removed. Keep it to a sentence or two of prose — the tool adds the metadata. The package ships stubs for the Noto families under `font_copywriter/data/stubs/`; pass your own folder to override them.

## License

Apache 2.0. See the [repository](https://github.com/twardoch/font-copywriter) for source.
