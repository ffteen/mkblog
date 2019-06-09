# -*- coding: utf-8 -*-
from setuptools import setup
import re
import os
import sys


long_description = (
    "mkblogs is a fast, simple and downright gorgeous static site generator, based on MkDocs "
)


def get_version(package):
    """Return package version as listed in `__version__` in `init.py`."""
    init_py = open(os.path.join(package, '__init__.py')).read()
    print(init_py)
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


def get_packages(package):
    """Return root package and all sub-packages."""
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]


setup(
    name="mkblog",
    version=get_version("mkblog"),
    license='BSD',
    description='Project documentation with Markdown.',
    long_description=long_description,
    author='ffteen',
    author_email='ffteen@qq.com',
    packages=get_packages("mkblog"),
    include_package_data=True,
    install_requires=[
        'click>=3.3',
        'Jinja2>=2.7.1',
        'livereload>=2.5.1',
        'lunr[languages]>=0.5.2',
        'Markdown>=2.3.1',
        'PyYAML>=3.10',
        'tornado>=5.0'
    ],
    python_requires='>=2.7.9,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*',
    entry_points={
        'console_scripts': [
            'mkblog = mkblog.__main__:cli',
        ],
        # 'mkdocs.themes': [
        #     'mkdocs = mkdocs.themes.mkdocs',
        #     'readthedocs = mkdocs.themes.readthedocs',
        # ],
        # 'mkdocs.plugins': [
        #     'search = mkdocs.contrib.search:SearchPlugin',
        # ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        'Topic :: Documentation',
        'Topic :: Text Processing',
    ],
    zip_safe=False,
)
