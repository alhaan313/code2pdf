from setuptools import setup, find_packages

setup(
    name="code2pdf",
    version="0.2",
    packages=find_packages(),  # Automatically find the 'code2pdf' package
    entry_points={
        'console_scripts': [
            'code2pdf = code2pdf.code2pdf:main',
        ],
    },
    install_requires=['pathspec'],
)
