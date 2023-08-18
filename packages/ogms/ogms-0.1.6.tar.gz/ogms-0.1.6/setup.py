from __future__ import print_function
from setuptools import setup, find_packages
import sys
from ogms import *

setup(
    name="ogms",
    version="0.1.6",
    author="Fengyuan Zhang",
    author_email="franklinzhang@foxmail.com",
    description="Python Framework",
    license="MIT",
    url="", 
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Environment :: Web Environment",
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: Microsoft',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    install_requires=[
        'requests>=2.22.0'
    ],
    zip_safe=True,
)