"""Setup configuration for Tic Tac Toe application."""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("tic_tac_toe/requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="tic-tac-toe-pro",
    version="1.0.0",
    author="Joseph",
    description="A professional web-based Tic Tac Toe game with AI opponents",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/TIC_TAC_TOE",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Games/Entertainment :: Board Games",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Framework :: Flask",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "tic-tac-toe=tic_tac_toe.app:main",
        ],
    },
)
