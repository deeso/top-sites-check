#!/usr/bin/env python
from setuptools import setup, find_packages
# configure the setup to install from specific repos and users
SVC_UTIL = 'https://github.com/deeso/service-utilities/tarball/' +\
           'master#egg=service-utilities-1.0.0'

DEPENDENCY_LINKS = [
    SVC_UTIL,
]

DESC = 'Python service to query domains from downloaded CSV files'
setup(name='top-sites-check',
      version='1.0',
      description=DESC,
      author='adam pridgen',
      author_email='dso@thecoverofnight.com',
      install_requires=['toml', 'distribute', 'regex', 'flask', ],
      packages=find_packages('src'),
      package_dir={'': 'src'},
      dependency_links=DEPENDENCY_LINKS,
      )
