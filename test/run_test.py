import sys
import os

# Ensure the parent directory is at the front of sys.path for local imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from code2pdf import main

if __name__ == "__main__":
    # Simulate CLI arguments for local code2pdf
    sys.argv = [
        "code2pdf",
        "test",  # folder to scan
        "-o", "test_code2pdf.pdf",
        "--title", "Test Folder Codebase",
        "--author", "Test Runner"
    ]
    main()
