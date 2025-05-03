import shutil
import subprocess
import markdown
import pdfkit
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Checks for required external dependencies (pandoc, xelatex).
# Exits the program if any are missing.
def check_dependencies():
    try:
        subprocess.run(["pandoc", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(["xelatex", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError as e:
        print(f"❌ Error: Missing dependency: {e.filename}. Please install it and try again.")
        exit(1)

# Converts a markdown file to PDF using pandoc and xelatex with the eisvogel template for a professional look.
def convert_to_pdf_pandoc(md_file, output_pdf):
    try:
        # Try to find eisvogel.latex in various locations
        eisvogel_path = os.path.abspath("eisvogel.latex")
        use_eisvogel = True
        if not os.path.isfile(eisvogel_path):
            pandoc_user_template_unix = os.path.expanduser("~/.pandoc/templates/eisvogel.latex")
            pandoc_user_template_win = os.path.join(
                os.environ.get("APPDATA", ""), "pandoc", "templates", "eisvogel.latex"
            )
            if os.path.isfile(pandoc_user_template_unix):
                eisvogel_path = pandoc_user_template_unix
            elif os.path.isfile(pandoc_user_template_win):
                eisvogel_path = pandoc_user_template_win
            else:
                print("⚠️ Warning: 'eisvogel.latex' template not found. Falling back to Pandoc's default template.")
                use_eisvogel = False

        pandoc_cmd = [
            "pandoc", md_file, "-o", output_pdf,
            "--pdf-engine=xelatex",
            "--highlight-style=pygments",
            "--variable", "mainfont=Times New Roman",
            "--variable", "monofont=Consolas",
            "--variable", "geometry:margin=1in",
            "--variable", "colorlinks=true",
            "--variable", "linkcolor=blue",
            "--toc",
            "--toc-depth=3",
        ]
        if use_eisvogel:
            print("📄 Using eisvogel template for PDF generation.")
            pandoc_cmd.insert(pandoc_cmd.index("--highlight-style=pygments"), "--template")
            pandoc_cmd.insert(pandoc_cmd.index("--template") + 1, eisvogel_path)

        subprocess.run(pandoc_cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: Failed to convert markdown to PDF using pandoc. {e}")
        exit(1)

# Converts markdown to PDF using reportlab (simple, no highlighting).
# Renders each line of the HTML-converted markdown.
def markdown_to_pdf(md_file, pdf_file):
    try:
        with open(md_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
        html_content = markdown.markdown(md_content)
        c = canvas.Canvas(pdf_file, pagesize=letter)
        text_object = c.beginText(72, 720)
        text_object.setFont("Helvetica", 12)
        for line in html_content.splitlines():
            text_object.textLine(line)
        c.drawText(text_object)
        c.save()
    except Exception as e:
        print(f"❌ Error: Failed to convert markdown to PDF using reportlab. {e}")
        exit(1)

# Converts markdown to PDF using pdfkit (via HTML).
# Reads markdown, converts to HTML, and generates a PDF.
def md_to_pdf(md_path, pdf_path):
    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        html_content = markdown.markdown(md_content)
        pdfkit.from_string(html_content, pdf_path)
    except Exception as e:
        print(f"❌ Error: Failed to convert markdown to PDF using pdfkit. {e}")
        exit(1)