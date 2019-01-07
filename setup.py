#!/usr/bin/env python3
import os
from setuptools import setup, find_packages

from nith_results import __version__, __mod_name__

with open("README.md", 'r') as f:
    long_description = f.read()
with open('requirements.txt', 'r') as f:
    requirements = [line.strip() for line in f.readlines()]

setup(
    name=__mod_name__,
    version=__version__,
    description='A Script to display results of nith',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Sarbjit Singh',
    author_email='srbcheema1@gmail.com',
    url='http://github.com/srbcheema1/'+__mod_name__,

    packages=find_packages(), # provides same list, looks for __init__.py file in dir
    include_package_data=True,
    install_requires=requirements, #external packages as dependencies

    entry_points={
        'console_scripts': [__mod_name__+'='+__mod_name__+'.main:main']
    },

    classifiers=[
        'Operating System :: POSIX :: Linux',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
    ],
    license='MIT License',
)
