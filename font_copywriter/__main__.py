#!/usr/bin/env python3
import fire

from .copywriter import copywrite


def cli():
    fire.core.Display = lambda lines, out: print(*lines, file=out)
    fire.Fire(copywrite)


if __name__ == "__main__":
    cli()
