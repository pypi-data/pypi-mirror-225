# Copyright (c) 2013, 2019, 2023 gocept gmbh & co. kg
# See also LICENSE.txt

# This should be only one line. If it must be multi-line, indent the second
# line onwards to keep the PKG-INFO file format intact.
"""
ZConfig statement to register a logging handler using WatchedFileHandler
"""

from setuptools import find_packages
from setuptools import setup


def read(name):
    """Read a file."""
    with open(name) as f:
        return f.read()


setup(
    name='zconfig_watchedfile',
    version='2.0',
    python_requires='>=3.8',
    install_requires=[
        'ZConfig',
        'setuptools',
    ],

    extras_require={
        'test': [
        ],
    },

    author='gocept <mail@gocept.com>',
    author_email='mail@gocept.com',
    license='ZPL 2.1',
    url='https://github.com/gocept/zconfig_watchedfile',
    keywords='ZConfig WatchedFileHandler logging handler',
    classifiers=[
        'License :: OSI Approved :: Zope Public License',
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    description=__doc__.strip(),
    long_description='\n\n'.join(read(name) for name in (
        'README.rst',
        'CHANGES.rst',
    )),
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
)
