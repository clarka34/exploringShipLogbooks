import os
from distutils.core import setup

# Get version and release info, which is all stored in shablona/version.py
ver_file = os.path.join('exploringShipLogbooks', 'version.py')
with open(ver_file) as f:
    exec(f.read())

opts = dict(name=NAME,
            description=DESCRIPTION,
            long_description=LONG_DESCRIPTION,
            url=URL,
            download_url=DOWNLOAD_URL,
            license=LICENSE,
            classifiers=CLASSIFIERS,
            version=VERSION,
            packages=PACKAGES,
            package_data=PACKAGE_DATA,
            requires=REQUIRES)


if __name__ == '__main__':
    setup(**opts)
