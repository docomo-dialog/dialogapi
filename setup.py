#! /usr/bin/env python
# coding:utf-8

from distutils.core import setup


setup(
    name="dialogapi",
    packages=["dialogapi", "dialogapi.test"],
    version="1.0.0",
    author="NTT DOCOMO, INC.",
    author_email="docomo-dialog-ml@nttdocomo.com",
    install_requires=[
        "requests==2.20.0",
        "fire==0.1.3",
        "Click==7.0",
        "PyYAML==4.2b1",
    ],
)
