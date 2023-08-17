#! /usr/bin/env python
"""The glmnet_classifier package setup file.

Directions

1.  Update the code and documentation

2.  Test the template by running test_template.py

3.  Update the documentation, including the jupyter notebooks

3.1 Convert the notebook content to rst and integrate it into quick_start.rst and user_guide.rst

    jupyter nbconvert quick_start.ipynb --to markdown --output README.md
    jupyter nbconvert quick_start.ipynb --to rst --output quick_start.rst
    jupyter nbconvert user_guide.ipynb --to rst --output user_guide.rst

3.2 Check the documentation by reading it from _build/html

4.  Remove the old distribution: rm -r dist

5. cd to glmnet_classifier and build the new dist folder:
python setup.py sdist bdist_wheel

Note that setup is deprecated and a replacement method is needed.

6. Upload to pip: twine upload dist/*

To build and use GLMnet.so:
The best practice to wrap Fortran code in Python,
is to export it to C first (see above) and then write this Cython code:
https://www.fortran90.org/src/best-practices.html#c-interface

"""

import codecs


import os
from setuptools import setup, find_packages

cmd = 'gfortran ./glmnet_python/GLMnet.f -fPIC -fdefault-real-8 -shared -o ./glmnet_python/GLMnet.so'
os.system(cmd)

# noinspection PyProtectedMember
from glmnet_classifier import _version

DISTNAME = 'glmnet_classifier'
DESCRIPTION = 'A binomial classifier based on glmnet'
with codecs.open('README.rst', encoding='utf-8-sig') as f:
    LONG_DESCRIPTION = f.read()
MAINTAINER = 'Carlson Research, LLC'
MAINTAINER_EMAIL = 'hrolfrc@gmail.com'
URL = 'https://github.com/hrolfrc/glmnet-classifier'
LICENSE = 'new BSD'
DOWNLOAD_URL = 'https://github.com/hrolfrc/glmnet-classifier'
VERSION = _version.__version__
INSTALL_REQUIRES = ['numpy', 'scipy', 'scikit-learn']
CLASSIFIERS = ['Intended Audience :: Science/Research',
               'Intended Audience :: Developers',
               'Development Status :: 2 - Pre-Alpha',
               'License :: OSI Approved',
               'Topic :: Scientific/Engineering',
               'Operating System :: Unix',
               'Programming Language :: Python :: 3']

EXTRAS_REQUIRE = {
    'tests': [
        'pytest',
        'pytest-cov'],
    'docs': [
        'sphinx',
        'sphinx-gallery',
        'sphinx_rtd_theme',
        'numpydoc',
        'matplotlib'
    ]
}

setup(name=DISTNAME,
      maintainer=MAINTAINER,
      maintainer_email=MAINTAINER_EMAIL,
      description=DESCRIPTION,
      license=LICENSE,
      url=URL,
      version=VERSION,
      download_url=DOWNLOAD_URL,
      long_description=LONG_DESCRIPTION,
      zip_safe=False,  # the package can run out of an .egg file
      classifiers=CLASSIFIERS,
      packages=find_packages(),
      package_data={"": ['*.so', './glmnet_classifier/*.so']},
      install_requires=INSTALL_REQUIRES,
      extras_require=EXTRAS_REQUIRE)
