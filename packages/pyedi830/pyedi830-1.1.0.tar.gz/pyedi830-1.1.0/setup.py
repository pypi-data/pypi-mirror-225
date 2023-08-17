""" Setup script for PythonEDI

"""
import re
from setuptools import setup, find_packages

LONG_DESCRIPTION = """Pyedi830 uses JSON format definitions to make it easy to parse and convert from EDI830 file to JSON and CSV file/data."""

setup(
    name="pyedi830",
    description="EDI 830 parser/converter",
    long_description=LONG_DESCRIPTION,
    url="https://github.com/dev0088/pyedi830",
    author="Ninja Dev",
    author_email="ninjadev999@gmail.com",
    license="MIT",
    version="1.1.0",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Plugins",
        "Intended Audience :: Developers",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Topic :: Office/Business",
        "Topic :: Text Processing"
    ],
    keywords="x12 edi 830",
    packages=['pyedi830', 'pyedi830.formats'],
    package_data={
        "pyedi830": ["formats/*.json"]
    },
    install_requires=['colorama', 'pandas'],
    include_package_data=True,
)
