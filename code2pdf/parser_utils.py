import argparse
from .constants import DEFAULT_OUTPUT

# Creates and returns the argument parser for the CLI.
# Encapsulates all argument definitions for modularity and reuse.
def create_parser():
    parser = argparse.ArgumentParser(
        description="📘 Convert the current directory's codebase into a syntax-highlighted PDF."
    )
    parser.add_argument(
        "folder", nargs="?", default=".",
        help="Directory to scan (default: current dir)"
    )
    parser.add_argument(
        "-o", "--output", default=DEFAULT_OUTPUT,
        help="Output PDF filename (default: codebase.pdf)"
    )
    parser.add_argument(
        "--title", default="📘 Project Codebase",
        help="Title for the PDF document"
    )
    parser.add_argument(
        "--author", default="Anonymous",
        help="Author name"
    )
    parser.add_argument(
        "--skip-empty", action="store_true",
        help="Skip empty files instead of showing them in the PDF"
    )
    parser.add_argument(
        "--no-toc", action="store_false",
        help="Disable table of contents in the PDF"
    )
    parser.add_argument(
        "--no-highlight", action="store_false",
        help="Disable syntax highlighting in the PDF"
    )
    parser.add_argument(
        "--include", help="Comma-separated list of file extensions to include (e.g. py,js,html)"
    )
    parser.add_argument(
        "--exclude", help="Comma-separated list of file extensions to exclude (e.g. log,pyc)"
    )
    parser.add_argument(
        "--project-desc", default=None,
        help="Project description to include in the PDF"
    )
    return parser
