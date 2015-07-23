# -*- coding: utf-8 -*-
from setuptools import setup


setup(
    name="jangle",
    description="AWS operations by cli should be simpler",
    author="Akira Chiku",
    author_email="akira.chiku@gmail.com",
    license="MIT License",
    url="https://github.com/achiku/jangle",
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "License :: OSI Approved :: MIT License"
    ],
    version='0.0.5',
    py_modules=['jangle'],
    include_package_data=True,
    install_requires=[
        'boto3==1.1.0',
        'click==4.1'
    ],
    entry_points={
        "console_scripts": [
            "jangle = jangle:cli",
        ],
    },
)
