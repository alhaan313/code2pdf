import os
import tempfile

# Constants for directories and files to exclude
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
TEMP_MD = os.path.join(tempfile.gettempdir(), 'combined_code.md')
