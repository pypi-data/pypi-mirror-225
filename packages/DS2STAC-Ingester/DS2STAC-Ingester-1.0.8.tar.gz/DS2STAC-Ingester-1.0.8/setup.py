#!/usr/bin/env python

"""Setup script for the DS2STAC-Ingester package."""

from setuptools import setup, find_packages
import versioneer
from setuptools import setup

setup(
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    long_description_content_type = 'text/x-rst',
    packages=['ds2stac_ingester'],
    install_requires=[requirement.strip() for requirement in open('requirements.txt').readlines()],

)

