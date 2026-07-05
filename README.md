# font-copywriter

Point it at a font. Get back a paragraph a human can read.

`font-copywriter` opens a font with [fontTools](https://github.com/fonttools/fonttools), pulls the family name, styles, glyph and character counts, designer, and licence out of the `name` and `cmap` tables, and writes a Markdown description. When a matching *stub* — a hand-written blurb for that family — is on hand, it goes in at the top. The prose carries the voice; the numbers carry the proof.

It also writes a small character specimen: the font's name over a stock pangram, trimmed to only the characters the font can actually draw.

![font-copywriter](docs/assets/icon.png)

## Install

Not on PyPI yet. Install from source:

```bash
pip install git+https://github.com/twardoch/font-copywriter
```

## Command line

```bash
font-copywriter <font_or_folder> <desc_path> [art_path] [stub_folder]
```

| Argument         | Meaning                                                              |
| ---------------- | ------------------------------------------------------------------- |
| `font_or_folder` | One font file (`.ttf`, `.otf`, `.ttc`, `.otc`) or a folder of them. |
| `desc_path`      | Folder for the generated `<Family>.md` descriptions.                |
| `art_path`       | Optional. Folder for the `<Family>.txt` specimens.                  |
| `stub_folder`    | Optional. Your own stubs. Omit to use the bundled Noto stubs.       |

```bash
# One font -> descriptions/NotoSans.md
font-copywriter NotoSans-Regular.ttf descriptions/

# Add a specimen in art/
font-copywriter NotoSans-Regular.ttf descriptions/ art/

# A whole folder, with your own stubs
font-copywriter fonts/ descriptions/ art/ my-stubs/
```

## In Python

```python
from font_copywriter import copywrite, read_metadata

# Just the facts
meta = read_metadata("NotoSans-Regular.ttf")
print(meta.family, meta.glyph_count, len(meta.characters))

# Write descriptions (and specimens), get back the paths written
written = copywrite("fonts/", "descriptions/", art_path="art/")
```

`read_metadata` returns a frozen `FontMetadata`: family, subfamily, full name, designer, copyright, licence, glyph count, and the sorted tuple of Unicode codepoints the font maps. Missing `name` records come back as empty strings, never `None`, so you never have to guard.

## Stubs

A stub is one Markdown file per family, named after the family with spaces removed — `Noto Sans` matches `NotoSans.md`. Matching folds both sides to lowercase letters and digits, so case and punctuation don't trip it up. Keep a stub to a sentence or two of prose; the tool adds the metadata underneath. Fonts without a matching stub still get a description — they just skip the blurb.

The package ships stubs for the Noto families under `src/font_copywriter/data/stubs/`. See that folder's `README.md` for the format.

## How it works

1. **Read** — fontTools opens each font; the `name` table gives family, styles, designer, and licence, the `cmap` gives the character set.
2. **Match** — the family name is folded and matched against the stub filenames. A hit supplies the blurb; a miss skips it.
3. **Write** — a description lands as `<Family>.md`; when an art folder is given, a specimen lands as `<Family>.txt` holding only drawable characters.

## Develop

```bash
uv venv && uv pip install -e ".[dev,test]"
uv run pytest                      # tests
uv run ruff check .                # lint
uv run mypy src/font_copywriter    # types
```

## License

Apache 2.0. See [LICENSE](LICENSE).
