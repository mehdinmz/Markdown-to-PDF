# Markdown to PDF

A simple Python tool to convert Markdown (`.md`) files into PDF documents using Playwright and Microsoft Edge.

Supports both **English (LTR)** and **Persian (RTL)** documents, with automatic PDF generation and A4 page formatting.

## Features

- Convert Markdown files to PDF.
- Support for English (Left-to-Right) and Persian (Right-to-Left).
- English is the default document direction.
- A4 page layout with configurable margins.
- Support for headings, paragraphs, lists, tables, links, and code blocks.
- Support for local images using relative paths.
- Code blocks are always displayed left-to-right.
- Uses Microsoft Edge through Playwright.
- Automatically generates the PDF in the same directory as the source file.

## Requirements

- Python 3.10 or newer
- Microsoft Edge installed on your system

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/markdown-to-pdf.git
cd markdown-to-pdf
```

Install the required dependencies:

```bash
py -m pip install markdown playwright
```

No separate Chromium installation is required. The application uses your installed Microsoft Edge browser.

## Usage

Run the script with the path to your Markdown file:

```bash
py md_to_pdf.py document.md
```

You will be asked to select the document direction:

```text
Select document direction:
1. English (LTR) - Default
2. Persian (RTL)

Your choice [1]:
```

- Press `Enter` or select `1` for English.
- Select `2` for Persian.

The generated PDF will be saved in the same directory as the input file.

### Specify an Output File

You can also specify a custom output path:

```bash
py md_to_pdf.py document.md -o output.pdf
```

## Examples

**English document:**

```bash
py md_to_pdf.py report.md
```

Select `1` or press Enter.

**Persian document:**

```bash
py md_to_pdf.py report-fa.md
```

Select `2`.

## Project Structure

```text
markdown-to-pdf/
├── md_to_pdf.py
├── requirements.txt
└── README.md
```

## License

This project is open-source. See the [LICENSE](LICENSE) file for details.

---

Made with Python.
