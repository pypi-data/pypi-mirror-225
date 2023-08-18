#!/bin/python3
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="reman",
    version="0.2.6",

    description="ReMan build tools",
    long_description=long_description,      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.6',                # Minimum version requirement of the package
    py_modules=["ReMan", "conanDefs"],             # Name of the python package
    install_requires=['mariadb', 'aptly-api-client'],                     # Install other dependencies if any
    packages=setuptools.find_packages(), #['Kuba_build_tools'],    # List of all python modules to be installed
    scripts=['bin/reman']
)
