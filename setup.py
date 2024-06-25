import os

from setuptools import find_packages, setup

VERSION = "2.2.0"


def read(fname):
    try:
        with open(os.path.join(os.path.dirname(__file__), fname)) as fh:
            return fh.read()
    except IOError:
        return ""


setup(
    name="python-datauri",
    version=VERSION,
    url="https://github.com/fcurella/python-datauri/",
    maintainer="Flavio Curella",
    maintainer_email="flavio.curella@gmail.com",
    description="A li'l class for data URI manipulation in Python",
    long_description=read("README.rst"),
    license="Unlicense",
    packages=find_packages(exclude=["tests", "*.tests"]),
    package_data={
        "faker": ["py.typed"],
    },
    platforms=["any"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: The Unlicense (Unlicense)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    test_suite="tests",
    install_requires=[
        "typing_extensions",
    ],
)
