from setuptools import setup

setup(name='pasteboard',
  install_requires=['pyobjc'],
  packages=['pasteboard'],
  description='inspect and manipulate macOS pasteboard',
  version='1.0.1',
  url='https://github.com/rolandcrosby/pasteboard',
  author='Roland Crosby',
  author_email='roland@rolandcrosby.com',
  license='ISC',
  scripts=['bin/pb'])