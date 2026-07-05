# this_file: src/font_copywriter/__init__.py
"""font-copywriter: turn a font's metadata into a human-readable description."""

from .copywriter import (
    FontMetadata,
    copywrite,
    default_stub_folder,
    read_metadata,
    render_description,
    render_specimen,
)

try:
    from .__version__ import version as __version__
except ImportError:  # not installed / no VCS metadata yet
    __version__ = "0.0.0"

__all__ = [
    "FontMetadata",
    "__version__",
    "copywrite",
    "default_stub_folder",
    "read_metadata",
    "render_description",
    "render_specimen",
]
