from setuptools import setup
from pathlib import Path
long_description = Path('./README.md').read_text()

setup(
  name='hak',
  version='1.2.4',
  license='MIT',
  description='Function Test Pair Toolbox',
  long_description=long_description,
  long_description_content_type='text/markdown',
  author='@JohnRForbes',
  author_email='john.robert.forbes@gmail.com',
  url='https://github.com/JohnForbes/hak',
  packages=['hak'],
  keywords='hak',
  install_requires=[],
)