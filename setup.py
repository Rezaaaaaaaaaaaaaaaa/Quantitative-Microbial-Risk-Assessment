#!/usr/bin/env python3
"""
Setup script for NIWA QMRA Assessment Toolkit
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_path = Path(__file__).parent / "README.md"
if readme_path.exists():
    with open(readme_path, "r", encoding="utf-8") as f:
        long_description = f.read()
else:
    long_description = "NIWA Quantitative Microbial Risk Assessment Toolkit"

# Read requirements from requirements.txt
requirements_path = Path(__file__).parent / "qmra_toolkit" / "requirements.txt"
requirements = []
if requirements_path.exists():
    with open(requirements_path, "r", encoding="utf-8") as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="niwa-qmra-toolkit",
    version="1.0.0",
    author="NIWA Earth Sciences",
    author_email="reza.moghaddam@niwa.co.nz",
    description="Quantitative Microbial Risk Assessment Toolkit - Python replacement for @Risk Excel functionality",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/niwa/qmra-toolkit",
    packages=find_packages(where="qmra_toolkit"),
    package_dir={"": "qmra_toolkit"},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.10",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.812",
            "sphinx>=4.0",
            "sphinx-rtd-theme>=1.0",
        ],
        "gui": [
            "tkinter",
        ],
    },
    entry_points={
        "console_scripts": [
            "qmra=src.qmra_toolkit:cli",
            "qmra-gui=src.qmra_gui:main",
            "qmra-enhanced-gui=src.enhanced_qmra_gui:main",
        ],
    },
    include_package_data=True,
    package_data={
        "qmra_toolkit": [
            "data/*.json",
            "data/*.yaml",
            "config/*.yaml",
            "templates/*.docx",
            "assets/*",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/niwa/qmra-toolkit/issues",
        "Source": "https://github.com/niwa/qmra-toolkit",
        "Documentation": "https://niwa-qmra-toolkit.readthedocs.io/",
    },
    keywords="microbiology risk assessment qmra niwa water quality pathogens",
    zip_safe=False,
)