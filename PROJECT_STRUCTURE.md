# Project Structure & File Purpose Guide

This document explains the purpose of important files and directories in this project, especially those related to **PyInstaller**, **Inno Setup**, and **Docker**.

---

## 📁 Directory Overview

```
.
├── code2pdf/                # Main Python package (source code)
├── build/                   # PyInstaller build artifacts
├── dist/                    # PyInstaller output executables
├── installers/              # (Optional) Inno Setup scripts or installer files
├── test/                    # Test scripts and sample files
├── code2pdf.egg-info/       # Packaging metadata (setuptools)
├── .vscode/                 # VSCode settings
├── README.md                # Main project documentation
├── setup.py                 # Python packaging script
├── Dockerfile               # (If present) Docker build instructions
└── ...
```

---

## 🐍 Python Packaging

- **`setup.py`**  
  Standard Python packaging script. Used for installing the `code2pdf` package via `pip`.  
  Generates the `code2pdf.egg-info/` directory.

- **`code2pdf/`**  
  Contains all main source code for the tool.

---

## 🧩 PyInstaller

- **Purpose:**  
  Converts your Python scripts into standalone executables for Windows (or other OSes).

- **Key Artifacts:**
  - **`dist/`**  
    Contains the final executable(s) produced by PyInstaller (e.g., `code2pdf.exe`).
  - **`build/`**  
    Temporary build files created by PyInstaller during the packaging process.
  - **`code2pdf.spec`**  
    (If present) PyInstaller configuration file, auto-generated or customized.

---

## 🏗️ Inno Setup

- **Purpose:**  
  Creates a Windows installer (`.exe` or `.msi`) that bundles your PyInstaller-built executable.

- **Key Files:**
  - **`code2pdf.iss`**  
    Inno Setup script. Defines how to package the executable, where to install, and what shortcuts to create.
  - **`installers/`**  
    (Optional) May contain the output installer or related scripts.

---

## 🐳 Docker

- **Purpose:**  
  (If present) Provides a containerized environment for running the tool, mainly for reproducibility or CI/CD.

- **Key Files:**
  - **`Dockerfile`**  
    Instructions for building a Docker image with all dependencies.

---

## 🧪 Testing

- **`test/`**  
  Contains test scripts and sample files to verify the tool's functionality.

---

## 📝 Other Files

- **`README.md`**  
  Main documentation for usage, features, and installation.

- **`.gitignore` / `.code2pdfignore`**  
  Ignore rules for Git and for the code2pdf tool itself.

- **`.vscode/`**  
  Editor-specific settings (safe to ignore for packaging/distribution).

---

## 🔑 Summary Table

| File/Folder             | Purpose                                                      |
|-------------------------|--------------------------------------------------------------|
| `setup.py`              | Python packaging/installation script                         |
| `code2pdf/`             | Main source code                                             |
| `dist/`                 | PyInstaller output executables                               |
| `build/`                | PyInstaller build temp files                                 |
| `code2pdf.spec`         | PyInstaller config (if present)                              |
| `code2pdf.iss`          | Inno Setup installer script                                  |
| `installers/`           | (Optional) Installer outputs/scripts                         |
| `Dockerfile`            | (Optional) Docker build instructions                         |
| `test/`                 | Test scripts and sample files                                |
| `README.md`             | Project documentation                                        |
| `.gitignore`            | Git ignore rules                                             |
| `.code2pdfignore`       | Ignore rules for code2pdf tool                               |
| `.vscode/`              | VSCode/editor settings                                       |

---

**Tip:**  
- Use `setup.py` for Python library installs.
- Use PyInstaller (`dist/`) for standalone executables.
- Use Inno Setup (`code2pdf.iss`) to create a Windows installer.
- Use Docker only if you want a containerized environment.

