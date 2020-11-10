#!/usr/bin/env python3

from setuptools import setup

requires = [line.strip() for line in open('requirements.txt').read().splitlines()]

setup(
    name='TTR-Launcher',
    version='0.1',
    description='A CLI launcher for Toontown Rewritten',
    author='Logan Swartzendruber',
    author_email='logan.swartzendruber@gmail.com',
    packages=['TTR-Launcher'],
    install_requires=requires,
)
