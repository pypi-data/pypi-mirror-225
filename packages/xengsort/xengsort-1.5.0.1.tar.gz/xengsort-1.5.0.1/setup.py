# coding: utf-8
NAME = "xengsort"

import sys
try:
    from setuptools import setup
except ImportError:
    print(f"Please install setuptools before installing {NAME}.", file=sys.stderr)
    exit(1)

if sys.version_info < (3,10):
    print(f"At least Python 3.10 is required for {NAME}.", file=sys.stderr)
    exit(1)


# load and set VERSION and DESCRIPTION
vcontent = open(f"{NAME}/_version.py").read()
exec(vcontent)

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    zip_safe=False,
    license='MIT',
    packages=[NAME],
    entry_points={
        "console_scripts": [
            f"{NAME} = {NAME}.{NAME}.{NAME}_main:main",
        ],
    },
    package_data={'': ['*.css', '*.sh', '*.html']},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Bio-Informatics"
    ]
)
