import pathspec
import argparse
import os
from datetime import datetime
from fnmatch import fnmatch  # at top of file
import subprocess
import tempfile
import shutil
import markdown
import pdfkit
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

EXCLUDE_DIRS = {
    '.git', 'node_modules', '__pycache__', 'venv', '.venv',
    '.mypy_cache', '.pytest_cache', '.idea', '.vscode', 'env', 
    'dist', 'build', '*.egg-info', 'installlers', 
    'out', 'tmp', 'temp', 'cache', 'logs', '.tox', '.coverage', 'dist', 
    'coverage.xml', 'htmlcov', 'pytest_cache', 'code2pdf.egg-info'
}
EXCLUDE_FILES = {
    '.DS_Store', 'Thumbs.db'
}

DEFAULT_OUTPUT = 'codebase.pdf'
# TEMP_MD = 'combined_code.md'
TEMP_MD = os.path.join(tempfile.gettempdir(), 'combined_code.md')


def load_ignore_spec(input_dir):
    ignore_file = None
    for fname in ['.gitignore', '.code2pdfignore']:
        candidate = os.path.join(input_dir, fname)
        if os.path.isfile(candidate):
            ignore_file = candidate
            break

    if ignore_file:
        with open(ignore_file, 'r') as f:
            patterns = f.read().splitlines()
        spec = pathspec.PathSpec.from_lines('gitwildmatch', patterns)
        print(f"📄 Using ignore patterns from: {os.path.basename(ignore_file)}")
        return spec
    else:
        print("⚙️ No ignore file found, using default exclusions.")
        return None

def format_path(path, backtick=True):
    path = path.replace('\\', '/')
    return f"`{path}`" if backtick else path.replace('_', r'\_')

def get_language(filename):
    ext = os.path.splitext(filename)[1]
    return {
        '.py': 'python', '.js': 'javascript', '.ts': 'typescript',
        '.html': 'html', '.css': 'css', '.java': 'java', '.cpp': 'cpp',
        '.c': 'c', '.json': 'json', '.sh': 'bash', '.rb': 'ruby',
        '.md': 'markdown', '.yml': 'yaml', '.yaml': 'yaml', '.xml': 'xml',
        '.txt': ''
    }.get(ext, '')

def generate_markdown(input_dir, title, author, out_file=TEMP_MD, 
                      skip_empty=False, ignore_spec=None,
                      include_exts=None, exclude_exts=None, 
                      include_names=None, exclude_names=None):
    date = datetime.now().strftime("%Y-%m-%d")
    with open(out_file, 'w', encoding='utf-8') as out:
        out.write(f"""
---
title: "{title}"
author: "{author}"
date: {date}
toc: true
toc-depth: 3
fontsize: 11pt
linkcolor: blue
---

""")
        for dirpath, dirnames, filenames in os.walk(input_dir):
            dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
            for filename in filenames:
                if (
                    filename in EXCLUDE_FILES or
                    filename.endswith(('.pyc', '.pyo', '.swp', '.tmp', '.log')) or
                    filename.startswith('.')
                ):
                    continue

                filename_only = os.path.basename(filename)
                ext = os.path.splitext(filename)[1].lstrip('.')

                if exclude_names and filename in exclude_names:
                    continue
                
                if exclude_exts and ext in exclude_exts:
                    continue
                
                if include_names and filename not in include_names:
                    if not (include_exts and ext in include_exts):
                        continue
                

                filepath = os.path.join(dirpath, filename)
                if filepath == out_file:
                    continue
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        lang = get_language(filename)

                        if not content.strip():
                            if skip_empty:
                                continue
                            out.write(f"\n## {format_path(filepath)}\n")
                            out.write("_No content available._\n\n")
                        else:
                            out.write(f"\n## {format_path(filepath)}\n")
                            out.write(f"```{lang}\n{content}\n```\n\n")
                except Exception as e:
                    print(f"⚠️ Skipping {filepath}: {e}")

def check_dependencies():
    for tool in ['pandoc', 'xelatex']:
        if not shutil.which(tool):
            print(f"❌ Missing dependency: {tool}")
            print("🔧 Please install it or ensure it's in your system PATH.")
            exit(1)

def convert_to_pdf_pandoc(md_file, output_pdf):
    try:
        subprocess.run([
            "pandoc", md_file, "-o", output_pdf,
            "--highlight-style=tango",
            "--pdf-engine=xelatex"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print("⚠️ Pandoc failed:", e)

def markdown_to_pdf(md_file, pdf_file):
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    html_content = markdown.markdown(md_content)
    c = canvas.Canvas(pdf_file, pagesize=letter)
    width, height = letter

    y_position = height - 40
    for line in html_content.splitlines():
        c.drawString(40, y_position, line)
        y_position -= 12

        
        if y_position < 40:
            c.showPage()
            y_position = height - 40

    c.save()

def md_to_pdf(md_path, pdf_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()

    html = markdown.markdown(md_text)
    pdfkit.from_string(html, pdf_path)


def main():
    # check_dependencies()

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


    args = parser.parse_args()
    folder_path = os.path.abspath(args.folder)

    if not os.path.isdir(folder_path):
        print(f"❌ Error: '{folder_path}' is not a valid directory.")
        return

    print(f"📁 Scanning: {folder_path}")
    ignore_spec = load_ignore_spec(folder_path)
    include_exts = set(args.include.split(',')) if args.include else None
    exclude_exts = set(args.exclude.split(',')) if args.exclude else None


    generate_markdown(
        folder_path, args.title, args.author, 
        skip_empty=args.skip_empty,
        ignore_spec=ignore_spec,
        include_exts=include_exts, 
        exclude_exts=exclude_exts
        )
    print(f"📝 Markdown compiled. Converting to PDF...")
    # convert_to_pdf_pandoc(TEMP_MD, args.output)
    md_to_pdf(TEMP_MD, args.output)
    # markdown_to_pdf(TEMP_MD, args.output)
    # convert_to_pdf_md2pdf(TEMP_MD, args.output)
    print(f"✅ Done! PDF saved as: {args.output}")

if __name__ == '__main__':
    main()
