# -*- coding: utf-8 -*-
"""Setup module."""
from typing import List
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def get_requires() -> List[str]:
    """Read requirements.txt."""
    requirements = open("requirements.txt", "r").read()
    return list(filter(lambda x: x != "", requirements.split()))


def read_description() -> str:
    """Read README.md and CHANGELOG.md."""
    try:
        with open("README.md") as r:
            description = "\n"
            description += r.read()
        with open("CHANGELOG.md") as c:
            description += "\n"
            description += c.read()
        return description
    except Exception:
        return '''Zenix is a lightweight tool for generating procedural noise such as white, pink, and brown noise.
        It can be used both as a command-line application and as a Python library, making it suitable for quick terminal
        usage as well as integration into Python projects. Zenix generates noise programmatically using NumPy and plays 
        it through an audio backend, allowing developers to create continuous background sound for focus, concentration, 
        relaxation, or acoustic masking. With support for multiple noise types, configurable parameters, fade-in effects, 
        and looping playback, Zenix provides a simple yet flexible way to work with procedural noise in both interactive 
        and programmatic environments.'''


setup(
    name='zenix',
    packages=['zenix'],
    version='0.1',
    description='Zenix: A Lightweight Tool for Procedural Noise Generation',
    long_description=read_description(),
    long_description_content_type='text/markdown',
    include_package_data=True,
    author='Sepand Haghighi',
    author_email='me@sepand.tech',
    url='https://github.com/sepandhaghighi/zenix',
    download_url='https://github.com/sepandhaghighi/zenix/tarball/v0.1',
    keywords="TODO",
    project_urls={
        'Source': 'https://github.com/sepandhaghighi/zenix'
    },
    install_requires=get_requires(),
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Other Audience',
        'Topic :: Utilities',
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Text Processing :: General",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    license='MIT',
    entry_points={
        'console_scripts': [
            'zenix = zenix.cli:main',
        ]}
)
