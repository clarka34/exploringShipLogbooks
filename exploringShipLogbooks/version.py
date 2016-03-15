from os.path import join as pjoin

# Format expected by setup.py and doc/source/conf.py: string of form "X.Y.Z"
_version_major = 0
_version_minor = 1
_version_micro = ''  # use '' for first of series, number for 1 and above
_version_extra = 'dev'
# _version_extra = ''  # Uncomment this for full releases

# Construct full version string from these.
_ver = [_version_major, _version_minor]
if _version_micro:
    _ver.append(_version_micro)
if _version_extra:
    _ver.append(_version_extra)

__version__ = '.'.join(map(str, _ver))

CLASSIFIERS = ["Intended Audience :: Science/Research",
               "License :: MIT License",
               "Operating System :: Mac OS",
               "Programming Language :: Python",
               "Topic :: Scientific/Engineering"]

# Description should be a one-liner:
description = "exploringShipLogbooks: explore old ship logbooks to gain a \
               greater understanding of the slave trade"
# Long description will go up on the pypi page
long_description = """

exploringShipLogbooks
========
To get started using this package, please go to the
repository README_.

.. _README: https://github.com/clarka34/exploringShipLogbooks/blob/master/README.md

License
=======
``exploringShipLogbooks`` is licensed under the terms of the MIT license.
See the file "LICENSE" for information on the history of this software, terms &
conditions for usage, and a DISCLAIMER OF ALL WARRANTIES.

All trademarks referenced herein are property of their respective holders.

Copyright (c) 2016--, clarka34
"""

NAME = "exploringShipLogbooks"
DESCRIPTION = description
LONG_DESCRIPTION = long_description
URL = "https://github.com/clarka34/exploringShipLogbooks"
DOWNLOAD_URL = ""
LICENSE = "MIT"
PLATFORMS = "Mac OS"
MAJOR = _version_major
MINOR = _version_minor
MICRO = _version_micro
VERSION = __version__
PACKAGES = ['exploringShipLogbooks',
            'exploringShipLogbooks.tests']
PACKAGE_DATA = {'exploringShipLogbooks': [pjoin('data', '*')]}
REQUIRES = ["numpy", "pandas"]
