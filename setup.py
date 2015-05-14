#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name='powerapp-pocket',
      version='0.1',
      packages=find_packages(),
      install_requires=['powerapp'],
      entry_points={
          'powerapp_services': [
              'service=powerapp_pocket',
          ],
      })
