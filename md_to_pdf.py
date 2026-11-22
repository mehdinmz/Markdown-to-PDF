
import argparse
import sys
from pathlib import Path

import markdown
from playwright.sync_api import sync_playwright


def get_text_direction():
    print("\nSelect document direction:")
    print("1. English (LTR) - Default")
    print("2. Persian (RTL)")

    choice = input("Your choice [1]: ").strip()

    if choice == "2":
        return "rtl", "right", "fa"

    return "ltr", "left", "en"


def get_css(direction, alignment):
    return f"""
    @page {{
        size: A4;
        margin: 20mm 18mm;
    }}

    body {{
        direction: {direction};
        text-align: {alignment};
        font-family: "Vazirmatn", Tahoma, Arial, sans-serif;
        font-size: 11pt;
        line-height: 1.8;
        color: #222;
        overflow-wrap: break-word;
    }}

    h1, h2, h3, h4, h5, h6 {{
        text-align: start;
        page-break-after: avoid;
        line-height: 1.4;
        margin-top: 1.2em;
    }}

    h1 {{
        font-size: 24pt;
        border-bottom: 1px solid #bbb;
        padding-bottom: 8px;
    }}

    h2 {{ font-size: 18pt; }}
    h3 {{ font-size: 14pt; }}

    p, li {{
        orphans: 3;
        widows: 3;
    }}

    a {{
        color: #1769aa;
        text-decoration: none;
        overflow-wrap: break-word;
    }}

    img {{
        max-width: 100%;
        height: auto;
    }}

    table {{
        width: 100%;
        border-collapse: collapse;
        margin: 1em 0;
        font-size: 9.5pt;
    }}

    th, td {{
        border: 1px solid #ccc;
        padding: 7px;
        text-align: start;
    }}

    th {{
        background: #eee;
    }}

    pre {{
        direction: ltr;
        text-align: left;
        white-space: pre-wrap;
        overflow-wrap: break-word;
        background: #f4f4f4;
        border: 1px solid #ddd;
        border-radius: 5px;
        padding: 10px;
        font-size: 9pt;
        page-break-inside: avoid;
    }}

    code {{
        direction: ltr;
        text-align: left;
        font-family: Consolas, "Courier New", monospace;
        background: #f2f2f2;
        padding: 2px 4px;
        border-radius: 3px;
    }}

    pre code {{
        background: transparent;
        padding: 0;
    }}

    blockquote {{
        border-left: 3px solid #999;
        margin: 1em 0;
        padding: 5px 12px;
        color: #555;
        background: #f8f8f8;
    }}

    hr {{
        border: 0;
        border-top: 1px solid #ccc;
        margin: 1.5em 0;
    }}
    """


def convert_markdown_to_pdf(input_file: Path, output_file: Path):

    if not input_file.is_file():
        raise FileNotFoundError(f"Input file not found: {input_file}")

    if input_file.suffix.lower() != ".md":
        raise ValueError("Input file must have a .md extension.")

    direction, alignment, language = get_text_direction()

    print("\nReading Markdown file...")

    markdown_text = input_file.read_text(encoding="utf-8")

    html_body = markdown.markdown(
        markdown_text,
        extensions=[
            "extra",
            "toc",
            "sane_lists",
            "nl2br",
        ],
        output_format="html5",
    )

    css = get_css(direction, alignment)

    base_uri = input_file.parent.as_uri().rstrip("/") + "/"

    html_document = f"""<!DOCTYPE html>
<html lang="{language}" dir="{direction}">
<head>
    <meta charset="UTF-8">
    <base href="{base_uri}">
    <title>{input_file.stem}</title>
    <style>
        {css}
    </style>
</head>
<body>
    {html_body}
</body>
</html>
"""

    print("Generating PDF...")

    with sync_playwright() as playwright:

        browser = playwright.chromium.launch(
            channel="msedge"
        )

        page = browser.new_page()

        page.set_content(
            html_document,
            wait_until="load"
        )

        page.pdf(
            path=str(output_file),
            format="A4",
            print_background=True,
            prefer_css_page_size=True,
        )

        browser.close()

    print("\nPDF created successfully!")
    print(f"Output: {output_file}")


def main():

    parser = argparse.ArgumentParser(
        description="Convert Markdown files to PDF."
    )

    parser.add_argument(
        "input",
        help="Path to Markdown file"
    )

    parser.add_argument(
        "-o",
        "--output",
        help="Output PDF path"
    )

    args = parser.parse_args()

    input_file = Path(args.input).expanduser().resolve()

    if args.output:
        output_file = Path(args.output).expanduser().resolve()

        if output_file.suffix.lower() != ".pdf":
            output_file = output_file.with_suffix(".pdf")

    else:
        output_file = input_file.with_suffix(".pdf")

    try:
        convert_markdown_to_pdf(
            input_file,
            output_file
        )

    except Exception as error:
        print(f"\nError: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()