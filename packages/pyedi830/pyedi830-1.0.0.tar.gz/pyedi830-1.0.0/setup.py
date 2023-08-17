""" Setup script for PythonEDI

"""
import re
from setuptools import setup, find_packages

setup(
    name="pyedi830",
    description="EDI 830 parser/converter",
    long_description="""pyedi830 uses JSON format definitions to make it easy
    to generate or read X12 EDI messages from/to Python dicts/lists.""",
    url="https://github.com/dev0088/pyedi830",
    author="Ninja Dev",
    author_email="ninjadev999@gmail.com",
    license="MIT",
    version="1.0.0",
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
    packages=find_packages(exclude=['test']),
    package_data={"pyedi830.formats": ["830_Forecast.json", "830.json", "ST.json"]},
    install_requires=['colorama', 'pandas'],
    include_package_data=True,
)
