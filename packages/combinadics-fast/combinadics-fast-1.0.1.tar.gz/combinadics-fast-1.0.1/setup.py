#!/usr/bin/env python

from distutils.core import setup

setup(name='combinadics-fast',
      version='1.0.1',
      description='Fast tool for converting unique numbers <-> unique k-combinations.',
      author='Andrew Healey',
      author_email='doolie.healey@gmail.com',
      url='https://github.com/andrew-healey/combinadics',
      py_modules=['combinadics_fast'],
      install_requires=['tqdm']
     )
