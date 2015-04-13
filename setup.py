#!/usr/bin/python

from distutils.core import setup

setup(name='BloggerEngine',
      version='1.0',
      description='A simple memory-persistent blogger engine.',
      author='Zack Zlotnik',
      author_email='zackzlotnik@gmail.com',
      package_dir={'bloggerengine': 'bloggerengine'},
      packages=['bloggerengine'],
      requires=['mock', 'flask', 'coverage'],
      data_files=[('scripts', 'run_tests.sh')]
)
