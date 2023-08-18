#!/usr/bin/env python

from setuptools import setup, find_packages
from setuptools.dist import Distribution

class BinaryDistribution(Distribution):
    def is_pure(self):
        return False

		
setup(name='afloat',
      version='0.1.1',
      description='A Fairly useful Library of Ocean Analysis Tools',
      author='Andrew Zulberti',
      author_email='andrew.zulberti@gmail.com',
      packages=find_packages(),
      install_requires=['numpy',
                        'matplotlib', 
                        'netcdf4', 
                        'scipy',
                        'xarray',
                        'utm',
                        'pyshp',],
      license='unlicensed to all but author',
      include_package_data=True,
      distclass=BinaryDistribution,
    )
