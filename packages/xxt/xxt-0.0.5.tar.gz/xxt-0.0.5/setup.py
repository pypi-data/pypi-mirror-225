from setuptools import setup

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# This call to setup() does all the work
setup(
    name="xxt",
    version="0.0.5",
    description="XXT is a multifunctional Python library designed to enhance various aspects of programming by providing an extensive set of functions and classes related to time, numbers, and randomization.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pythonraft1575.github.io/xxt/",
    author="Xi Teo",
    author_email="diamondraft1575@gmail.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent"
    ],
    packages=["xxt"],
    include_package_data=True,
    install_requires=["datetime", "openai", "qrcode"]
)