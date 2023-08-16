from setuptools import setup

# read the contents of README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name = 'python-brickscout-api',         
  packages=['brickscout', 'brickscout.models', 'brickscout.constants', 'brickscout.endpoints', 'brickscout.cache'],
  version = '1.1.1',
  license='GPL-3.0-or-later',
  description = 'Wrapper for the BrickScout API',
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'Alexander Schillemans',
  author_email = 'alexander.schillemans@hotmail.com',
  url = 'https://github.com/alexanderlhsglobal/python-brickscout-api',
  download_url = 'https://github.com/alexanderlhsglobal/python-brickscout-api/archive/refs/tags/1.1.1.tar.gz',
  keywords = ['brickscout', 'brick', 'scout', 'brick scout', 'lego', 'api'],
  install_requires=[
          'requests',
          'requests_oauthlib',
          'jsonpatch',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    'Programming Language :: Python :: 3.10',
  ],
)