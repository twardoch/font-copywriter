# Plan

## Status

The v1 goal — make the tool actually work, and give it modern scaffolding — is
done. `copywrite()` reads real font metadata and writes descriptions and
specimens; packaging, tests, CI, and docs are in place. What remains is
depth: better descriptions and richer output.

## Next: make the description say something

Today a font with no matching stub gets facts (styles, counts, designer,
licence) but no prose. The highest-value next step is to derive a sentence from
the font itself:

1. **Script detection.** From the `cmap` codepoints, map to Unicode blocks and
   collapse to script names (Latin, Cyrillic, Greek, Arabic, …). fontTools
   exposes `unicodedata` helpers; `fontTools.unicodedata.script()` maps a
   codepoint to a script tag. Count coverage per script, keep the ones the font
   substantially supports.
2. **Style read.** Use the OS/2 and `head` tables (weight class, width class,
   italic bit) to describe the style beyond the `name` string.
3. **Compose.** With scripts and style in hand, write a single generated
   sentence — "A bold sans-serif covering Latin, Greek, and Cyrillic." — used
   when no stub matches.

## Then: real specimens

Replace the plain-text specimen with a rendered one. `fontTools` plus a
rasterizer (e.g. `freetype-py` or `blackrenderer`) can draw a waterfall PNG or
SVG. Keep it optional and behind the existing `art_path` argument so the
text path stays dependency-light.

## Family grouping

A folder of `Family-Regular`, `-Bold`, `-Italic` should collapse to one
description that lists every style, rather than one file per face. Group by
typographic family name before writing.

## Publish

Once descriptions read well, enable PyPI publishing in `release.yml` (trusted
publishing, `id-token: write`) and drop the "not on PyPI yet" note from the
README and docs.
