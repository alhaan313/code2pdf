import argparse
import os

from .file_utils import (
    load_ignore_spec,
    format_path,
    get_language,
    generate_markdown,
)
from .pdf_utils import (
    check_dependencies,
    convert_to_pdf_pandoc,
    markdown_to_pdf,
    md_to_pdf,
)
from .constants import (
    EXCLUDE_DIRS,
    EXCLUDE_FILES,
    DEFAULT_OUTPUT,
    TEMP_MD,
)
from .parser_utils import create_parser

def main():
    # Main entry point: parses arguments, generates markdown, and converts to PDF.
    # Handles user input and orchestrates the codebase-to-PDF workflow.

    parser = create_parser()  # use modularized parser
    args = parser.parse_args()
    folder_path = os.path.abspath(args.folder)

    if not os.path.isdir(folder_path):
        print(f"❌ Error: '{folder_path}' is not a valid directory.")
        return

    print(f"📁 Scanning: {folder_path}")
    ignore_spec = load_ignore_spec(folder_path)
    include_exts = set(args.include.split(',')) if args.include else None
    exclude_exts = set(args.exclude.split(',')) if args.exclude else None

    # Determine output PDF path: if user gave just a filename, put it in the scanned folder
    output_arg = args.output
    if not os.path.isabs(output_arg):
        output_pdf = os.path.join(folder_path, output_arg)
    else:
        output_pdf = output_arg

    generate_markdown(
        folder_path, args.title, args.author, 
        skip_empty=args.skip_empty,
        ignore_spec=ignore_spec,
        include_exts=include_exts, 
        exclude_exts=exclude_exts,
        project_desc=args.project_desc,
        tool_version="0.2"
    )
    print(f"📝 Markdown compiled. Converting to PDF...")
    convert_to_pdf_pandoc(TEMP_MD, output_pdf)
    # md_to_pdf(TEMP_MD, output_pdf)
    # markdown_to_pdf(TEMP_MD, output_pdf)
    print(f"✅ Done! PDF saved as: {output_pdf}")

if __name__ == '__main__':
    main()
