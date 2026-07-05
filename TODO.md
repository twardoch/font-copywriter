# TODO

Bigger ideas beyond the v1 modernization. See `PLAN.md` for detail.

- [ ] Richer metadata: detect supported scripts/Unicode blocks and name them in the description (e.g. "Latin, Cyrillic, Greek"), so a font with no stub still gets a real sentence.
- [ ] Auto-generate a stub sentence from scripts + style when no stub matches, instead of only listing facts.
- [ ] Real "art": render a PNG/SVG waterfall specimen (via `fontTools` + a rasterizer) rather than a plain-text sample.
- [ ] Group faces of one family: fold `NotoSans-Regular`, `-Bold`, `-Italic` into a single description listing every style.
- [ ] Publish to PyPI once the description output is judged good enough (enable the PyPI job in `release.yml`).
- [ ] Variable-font awareness: report axes and named instances from `fvar`.
