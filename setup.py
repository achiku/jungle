# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='jangle',
    py_modules='jangle',
    install_requires=open('requirements.txt').read().splitlines(),
    entry_points={
        "console_scripts": [
            "jangle = jangle:cli",
        ],
    },
)
