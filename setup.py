#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='pomma',
    version='0.1a',
    description=('Partially Observable Markov Models with Adaptation'),
    author='Dezhe Jin, David Nicholson',
    author_email='https://github.com/NickleDave/pomma/issues',
    url='https://github.com/NickleDave/pomma/',
    packages=find_packages(),
    license='BSD',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.6',
    ]
    )
