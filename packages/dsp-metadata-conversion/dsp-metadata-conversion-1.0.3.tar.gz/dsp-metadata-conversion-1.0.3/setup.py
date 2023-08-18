from setuptools import setup, find_packages
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="dsp-metadata-conversion",
    version="1.0.3",
    description="ython CLI for converting project metadata from JSON to RDF",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dasch-swiss/dsp-metadata-conversion",
    author="Balduin Landolt",
    author_email="balduin.landolt@dasch.swiss",
    license="Apache 2.0",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9.0",
    install_requires=[
        "isodate==0.6.0",
        "owlrl==5.2.3",
        "prettytable==2.2.1; python_version >= '3.6'",
        "pyparsing==3.0.1; python_version >= '3.6'",
        "pyshacl==0.17.2",
        "rdflib==6.0.2",
        "six==1.16.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "wcwidth==0.2.5",
    ],
    entry_points={
        "console_scripts": ["convert-metadata=converter.converter:cli", ],
    },
    include_package_data=True,
    zip_safe=False,
)
