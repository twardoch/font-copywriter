# font-copywriter

`font-copywriter` is a Python tool designed to generate human-readable descriptions for font families. It aims to simplify the process of creating informative and consistent documentation for fonts, which can be especially useful for large font collections like the Noto font family.

## What it does

The primary goal of `font-copywriter` is to analyze font files (or collections of font files within a folder) and produce descriptive text that outlines their characteristics, intended use, and other relevant details. This can include information about the supported scripts, stylistic features, and any unique aspects of the font family.

### Key Features (Planned)

*   Extraction of detailed font metadata.
*   Integration with user-provided Markdown stubs/templates.
*   Generation of descriptions in Markdown format.
*   Command-line interface and Python library usage.
*   Support for processing individual font files and entire folders.
*   (Potentially) Generation of "art" files like text samples or glyph waterfalls.

## Who it's for

This tool is beneficial for:

*   **Typographers and Font Designers:** To automatically generate baseline descriptions for their creations.
*   **Software Developers:** Who need to integrate font information into applications or websites.
*   **Localization and Internationalization Teams:** Working with diverse font families for different languages and scripts.
*   **Content Creators and Designers:** To help them understand and choose appropriate fonts for their projects.

## Why it's useful

`font-copywriter` offers several advantages:

*   **Consistency:** Ensures that font descriptions are uniform and follow a standard format.
*   **Efficiency:** Automates the often time-consuming task of writing font descriptions manually.
*   **Accessibility:** Provides clear and understandable information about fonts, making them more accessible to a wider audience.
*   **Documentation:** Facilitates better documentation practices for font projects.

## Installation

As `font-copywriter` is a Python package, you can install it using `pip`. It is recommended to install it in a virtual environment.

```bash
pip install font-copywriter
```

*(Note: Once the package is published on PyPI, this command will work. For local development, you might use `pip install .` from the root of the repository.)*

## How to use

`font-copywriter` can be used both as a command-line tool and as a Python library.

### Command-Line Interface (CLI)

The tool provides a command-line interface for easy generation of font descriptions.

```bash
font-copywriter <font_path_or_folder> <desc_path> <art_path> <stub_folder>
```

**Arguments:**

*   `font_path_or_folder`: Path to a single font file or a folder containing multiple font files.
*   `desc_path`: Path where the generated description file(s) will be saved.
*   `art_path`: Path related to "art" files (the exact nature of these needs further clarification based on implementation, but it could refer to sample images, character sets, or other visual representations).
*   `stub_folder`: Path to a folder containing stub files (e.g., Markdown templates or partial descriptions) that can be used to guide or supplement the generation process. The `font_copywriter/data/stubs/` directory in this repository provides examples, primarily for Noto fonts.

**Example:**

```bash
font-copywriter "path/to/your/fonts" "output/descriptions" "output/art" "path/to/stubs"
```

### Programmatic Usage (Python Library)

You can also integrate `font-copywriter` into your Python projects by importing the `copywrite` function:

```python
from pathlib import Path
from font_copywriter import copywrite

# Define the paths
font_source = Path("path/to/your/fonts_folder_or_file")
description_output_path = Path("output/font_descriptions")
art_output_path = Path("output/font_art")
stubs_directory = Path("path/to/your/stubs")

# Ensure output directories exist if needed by the function's implementation
description_output_path.mkdir(parents=True, exist_ok=True)
art_output_path.mkdir(parents=True, exist_ok=True)

# Generate the description
# Note: The exact behavior (e.g., return value, how files are saved)
# will depend on the implementation of the copywrite function.
copywrite(
    font_path_or_folder=font_source,
    desc_path=description_output_path,
    art_path=art_output_path,
    stub_folder=stubs_directory
)

print(f"Font descriptions generated in {description_output_path}")
```

---

## Technical Details

This section provides a more in-depth look at how `font-copywriter` is structured and intended to operate. As the project is in its early stages, some of these details are based on the planned architecture and may evolve.

### How it Works (Intended Architecture)

The core logic resides in the `copywrite` function within `font_copywriter/copywriter.py`. The intended process is as follows:

1.  **Font Analysis:** The tool will inspect the font file(s) provided in `font_path_or_folder`. This likely involves using font-parsing libraries (e.g., `fontTools`) to extract metadata such as:
    *   Family name, style, weight, width
    *   Supported Unicode ranges and scripts
    *   Glyph counts
    *   OpenType features
    *   Copyright and licensing information

2.  **Stub Integration:** If a relevant stub file is found in the `stub_folder` (e.g., matching the font family name), its content will be used as a template or starting point for the description. The stub files (currently Markdown files in `font_copywriter/data/stubs/`) allow for pre-defined text or structure to be incorporated.

3.  **Description Generation:** Based on the analyzed font data and any integrated stub content, a human-readable description is composed. This might involve:
    *   Filling in placeholders in a template.
    *   Programmatically generating sentences or paragraphs based on font characteristics.
    *   Formatting the output (likely as Markdown).

4.  **"Art" File Handling:** The `art_path` argument suggests functionality related to generating or managing associated visual materials. This could include:
    *   Creating sample text renderings.
    *   Generating waterfall specimens.
    *   Listing key glyphs or character sets.
    *   The exact nature of "art" files will be defined as the tool is developed.

5.  **Output:** The generated description(s) will be saved to the location specified by `desc_path`. If multiple fonts are processed from a folder, it might create multiple description files or a single consolidated one.

### Project Structure

*   `font_copywriter/`: Main package directory.
    *   `__init__.py`: Initializes the package and exports the version.
    *   `__main__.py`: Provides the CLI entry point using `python-fire`.
    *   `copywriter.py`: Contains the core `copywrite` function (currently a stub).
    *   `data/stubs/`: Contains example stub files, primarily for Noto fonts. These seem to be Markdown files that can serve as templates.
*   `requirements.txt`: Lists Python dependencies (currently empty, but will likely include font analysis tools).
*   `setup.py`: Standard Python package setup file.
*   `README.md`: This file.
*   `LICENSE`: Apache 2.0 License.

### Input and Output

*   **Input:**
    *   `font_path_or_folder (Path | str)`: Path to a font file (e.g., `.ttf`, `.otf`) or a directory containing font files.
    *   `desc_path (Path | str)`: Output directory or file path for the generated descriptions.
    *   `art_path (Path | str)`: Output directory or file path for "art" files.
    *   `stub_folder (Path | str)`: Path to a directory containing stub/template files (e.g., `.md`).
*   **Output:**
    *   Human-readable font description files (likely Markdown).
    *   Associated "art" files (format to be determined).

### Coding Conventions

While not explicitly stated, the project follows standard Python conventions (PEP 8). Key points for contributors:

*   Use type hinting (`from typing import ...`).
*   Write clear and concise code.
*   Include docstrings for modules, classes, and functions.
*   Ensure code is well-tested (though tests are not yet present).

### Contributing

Contributions to `font-copywriter` are welcome! As the project is in its early stages, there are many opportunities to help shape its development.

1.  **Reporting Bugs:** If you find a bug, please open an issue on the GitHub repository. Include:
    *   Steps to reproduce the bug.
    *   Expected behavior.
    *   Actual behavior.
    *   Your environment (OS, Python version).

2.  **Suggesting Enhancements:** Have an idea for a new feature or an improvement to an existing one? Open an issue to discuss it.

3.  **Pull Requests:**
    *   Fork the repository.
    *   Create a new branch for your feature or bug fix: `git checkout -b feature/your-feature-name` or `git checkout -b fix/your-bug-fix`.
    *   Make your changes.
    *   Add tests for your changes.
    *   Ensure your code lints and tests pass.
    *   Commit your changes with a clear and descriptive commit message.
    *   Push your branch to your fork: `git push origin feature/your-feature-name`.
    *   Open a pull request against the `main` branch of the original repository.

When contributing code, please ensure your changes align with the project's goals and coding conventions. If the `copywriter.py` function is implemented, ensure your contributions are compatible with its intended functionality.

*(Note: As `CLAUDE.md` was mentioned in the prompt but is not present in the file listing, no specific instructions from it could be incorporated. If such a file exists or is created, its guidelines should be followed.)*

---

## License

`font-copywriter` is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for more details.
