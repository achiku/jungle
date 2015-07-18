# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

setup(
    name='jangle',
    packages=find_packages(),
    install_requires=open('requirements.txt').read().splitlines(),
    entry_points={
        "console_scripts": [
            "jangle = djangle.__main__:main",
        ],
    },
)
