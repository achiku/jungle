# -*- coding: utf-8 -*-
"""AWS operations by cli should be simpler."""
from setuptools import find_packages, setup

setup(
    name='jangle',
    version='0.0.11',
    url='https://github.com/achiku/jangle',
    license='BSD',
    author='Akira Chiku',
    author_email='akira.chiku@gmail.com',
    description='AWS operations by cli should be simpler',
    long_description=__doc__,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'boto3==1.1.0',
        'click==4.1'
    ],
    entry_points={
        'console_scripts': [
            'jangle = jangle.cli:cli',
        ],
    },
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        # 'Operating System :: Windows',
        # 'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
