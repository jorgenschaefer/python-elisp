#!/usr/bin/env python

from setuptools import setup

import elisp

with open("README.rst") as f:
    long_description = f.read()

setup(
    name="elisp",
    version=elisp.__version__,
    description="Emacs Lisp parser",
    long_description=long_description,
    url="https://github.com/jorgenschaefer/elisp",
    license="LGPL",
    author="Jorgen Schaefer",
    author_email="contact@jorgenschaefer.de",
    packages=["elisp"],
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Emacs-Lisp",
        ("License :: OSI Approved :: "
         "GNU Lesser General Public License v3 or later (LGPLv3+)")
    ],
    install_requires=[
        "grako"
    ],
    test_suite="elisp"
)
