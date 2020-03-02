# coding: utf8

from setuptools import setup

setup(name='mower',
      version='0.1',
      description='Move a mower around',
      author='Quentin Augé',
      author_email='quentin.auge@gmail.com',
      license='closed',
      py_modules=['mower'],

      python_requires='>=3.6',

      classifiers=['Programming Language :: Python :: 3 :: Only',
                   'Operating System :: MacOS',
                   'Operating System :: Unix'],

      extras_require={
          'testing': ['coverage', 'pytest', 'pytest-cov']
      },

      entry_points={
          'console_scripts': [
              'mower = mower:main'
          ]
      })
