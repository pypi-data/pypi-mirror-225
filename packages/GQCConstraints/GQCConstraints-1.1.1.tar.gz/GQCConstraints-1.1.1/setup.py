import setuptools
import os
import sys


# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
long_description = long_description.split('\n', 8)[8]

setuptools.setup(
      name='GQCConstraints',
      version='1.1.1',
      description='This library build on GQCP provides easy to work with utilities in order to perform constrained quantum chemical calculations.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='The Ghent Quantum Chemistry Group',
      packages=setuptools.find_packages(),
      install_requires=['pandas==1.2.5', 'numpy==1.22.4', 'scipy==1.7.0'],
      keywords=['quantum chemistry', 'constraints', 'GQCP']
      )
