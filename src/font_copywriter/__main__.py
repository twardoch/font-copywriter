#!/usr/bin/env python3
# this_file: src/font_copywriter/__main__.py
"""Command-line entry point.

    font-copywriter <font_or_folder> <desc_path> [art_path] [stub_folder]

Feeds the arguments straight to `copywrite`. Omit `stub_folder` to use the
bundled Noto stubs.
"""

import fire  # type: ignore[import-untyped]

from .copywriter import copywrite


def cli() -> None:
    """Expose `copywrite` as a CLI via python-fire."""
    fire.core.Display = lambda lines, out: print(*lines, file=out)
    fire.Fire(copywrite)


if __name__ == "__main__":
    cli()
