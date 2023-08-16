from distutils.core import setup
from setuptools import find_packages

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
  name = 'cave_utils',
  packages=['cave_utils'],
  version = '1.6.1',
  license='MIT',
  description = 'Cave utilities for the CAVE App at the MIT',
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'Connor Makowski',
  author_email = 'connor.m.makowski@gmail.com',
  url = 'https://github.com/mit-cave/cave_utils',
  download_url = 'https://github.com/mit-cave/cave_utils/dist/cave_utils-1.6.1.tar.gz',
  keywords = [],
  install_requires=[
    'pamda>=2.1.2',
  ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
  ],
  python_requires=">=3.7, <4",
)
