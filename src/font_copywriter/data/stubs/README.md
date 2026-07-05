# Stub files

A stub is a hand-written Markdown blurb for one font family. `font-copywriter`
looks one up by folding the font's family name to lowercase letters and digits
(`Noto Sans` → `notosans`) and matching it against the stub filename
(`NotoSans.md` → `notosans`). On a hit, the stub's text is dropped in near the
top of the generated description, above the metadata facts.

The format is deliberately plain: one file per family, named after the family
with spaces removed, holding whatever prose you want the tool to reuse. Keep it
to a sentence or two — the metadata (styles, glyph and character counts,
designer, licence) is added automatically.

Example — `NotoSans.md`:

```markdown
Noto Sans is an unmodulated (“sans serif”) design for texts in the _Latin,
Cyrillic_ and _Greek_ scripts.
```

Fonts without a matching stub still get a description; they just skip the blurb.
