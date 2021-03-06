#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'selenium==3.4.2',
]

test_requirements = [
    #'ipython==5.*',
    'mock',
]

setup(
    name='seleniumpy',
    version='0.2.1',
    description="SeleniumPy is a pythonic wrapper around the selenium API",
    long_description=readme + '\n\n' + history,
    author="Ryan Nowakowski",
    author_email='tubaman@fattuba.com',
    url='https://github.com/tubaman/seleniumpy',
    packages=[
        'seleniumpy',
    ],
    package_dir={'seleniumpy':
                 'seleniumpy'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD license",
    zip_safe=False,
    keywords='seleniumpy',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
