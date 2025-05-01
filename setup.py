from setuptools import setup

setup(
    name="code2pdf",
    version="0.2",
    py_modules=["code2pdf"],
    entry_points={
        'console_scripts': [
            'code2pdf = code2pdf:main',
        ],
    },
    install_requires=['pathspec'],
)
