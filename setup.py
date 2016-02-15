import os
from distutils.core import setup

opts = dict(description='Ship logbook project',
            packages=['exploring-ship-logbooks','exploring-ship-logbooks/tests']
            )

if __name__ == '__main__':
    setup(**opts)
