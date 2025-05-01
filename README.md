# 🧾 code2pdf

**Convert entire codebases into syntax-highlighted PDFs with ease.**

---

## 📌 Overview

`code2pdf` is a Python-based command-line tool that scans your source code directory, compiles it into a Markdown file with proper formatting and syntax highlighting, and finally converts it to a styled PDF using **Pandoc** with the **XeLaTeX** engine.

It’s ideal for creating technical documentation, sharing annotated codebases, or archiving projects in a readable PDF format.

---

## 🛠️ Features

- 📂 Recursive directory scanning with ignore support (`.gitignore`, `.code2pdfignore`)
- 🧠 Auto syntax highlighting via file extensions
- 📑 Markdown generation for full code structure
- 📄 Table of contents, metadata, and formatting options
- 🧵 Supports `--include`, `--exclude`, and `--skip-empty` flags
- 📦 Inno Setup-based Windows installer for one-click install
- ⚙️ Optional library installation with `setup.py` (requires local Pandoc + XeLaTeX)

---

## ⚙️ How It Works

### 1. 🐍 Python → Markdown

The script walks through the project directory and:

- Applies ignore patterns (from `.gitignore` or `.code2pdfignore`)
- Collects files based on extensions or names
- Wraps code in Markdown fenced blocks with proper language tags
- Optionally skips empty files

This is written to a temporary or designated Markdown file like `combined_code.md`.

---

### 2. 📝 Markdown → PDF

The generated Markdown is converted to PDF using **Pandoc** with the **XeLaTeX** engine for:

- Accurate font rendering  
- Cross-platform support  
- Beautiful styling with TOC, headers, links, etc.

Example command:

```bash
pandoc combined_code.md -o output.pdf --pdf-engine=xelatex --highlight-style=tango
```

> 📌 **Note:** `pandoc` and `xelatex` must be installed locally and accessible via PATH.

---

## 📦 Packaging Options

### 🔹 A. Python Library

You can install `code2pdf` as a Python library using:

```bash
pip install .
```

But this only works if:

- `pandoc` and `xelatex` are already installed on the system.
- The user manually manages the dependencies.

---

### 🔹 B. Standalone Windows Installer (Recommended)

Due to the dependency on local Pandoc and LaTeX binaries, we package the CLI using:

- [`PyInstaller`](https://pyinstaller.org/) to create an executable
- [`Inno Setup`](https://jrsoftware.org/isinfo.php) to create a proper `.exe` installer

This installer:

- Bundles the `code2pdf` executable
- Optionally checks or guides the user to install Pandoc/XeLaTeX
- Adds it to PATH for CLI access

#### Inno Setup Example Snippet (`code2pdf.iss`)

```pascal
[Setup]
AppName=code2pdf
AppVersion=1.0
DefaultDirName={pf}\code2pdf
DefaultGroupName=code2pdf

[Files]
Source: "dist\code2pdf.exe"; DestDir: "{app}"

[Icons]
Name: "{group}\code2pdf CLI"; Filename: "{app}\code2pdf.exe"
```

Then compile using **Inno Setup Compiler**.

---

## 🐳 Why Not Docker?

We considered Docker, but it introduces challenges:

- Pandoc + XeLaTeX images are **heavy** (~1.5 GB)
- Not practical for end-users wanting **PDF output on their host OS**
- GUI PDF viewers and access to local files are restricted in containers
- More steps required for volume mounting and output copying

Hence, **native installation** remains the better option for usability.

---

## 🚀 Usage

### CLI

```bash
code2pdf --title "My Project" --author "Jane Doe" --include py,js,html
```

### Options

```
-o, --output        Output PDF filename  
--title             Title for the PDF  
--author            Author name  
--include           Comma-separated file extensions to include  
--exclude           Comma-separated file extensions to exclude  
--skip-empty        Skip empty files  
--no-toc            Disable table of contents  
--no-highlight      Disable syntax highlighting  
```

---

## 📋 Example

```bash
code2pdf my_project --title "Code Snapshot" --author "Adeel" --include py,md --skip-empty
```

---

## 📎 Requirements

- Python 3.7+
- [Pandoc](https://pandoc.org/)
- [TeX Live / MikTeX (with XeLaTeX)](https://www.latex-project.org/get/)

Optional (for building the installer):

- [PyInstaller](https://pyinstaller.org/)
- [Inno Setup](https://jrsoftware.org/isinfo.php)

---

## 💡 Tips

- Create a `.code2pdfignore` to exclude folders/files like `venv`, `node_modules`, etc.
- Always test large projects with Pandoc manually first to avoid XeLaTeX buffer issues.
- For large codebases, consider splitting Markdown files before PDF generation if needed.

---

## 📁 Project Structure

```
code2pdf/
├── code2pdf.py        # Main CLI tool  
├── setup.py           # Python packaging  
├── code2pdf.iss       # Inno Setup script  
├── README.md          # You're reading it!  
└── assets/            # Optional logo or icons  
```

---

## 🧠 Contributing

Feel free to fork and submit PRs. Suggestions and improvements are welcome!

---

## 📝 License

MIT License © 2025
```

---

Let me know if you want this split into separate files, or if you'd like badges, screenshots, demo GIFs, or a logo added for open source publishing!
