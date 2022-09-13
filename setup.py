#!/usr/bin/env python3

from setuptools import setup


__version__ = '0.0.2'


setup(
    name='memor-client',
    version=__version__,
    description='Easily store and retrieve important small data like URLs or names',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Cléber Zavadniak',
    python_requires='>=3.8',
    author_email='contato@cleber.solutions',
    url='https://memor.cleber.solutions',
    entry_points={'console_scripts': ['memor=memor.main:cli']},
    packages=['memor'],
    install_requires=[
        'requests >= 2.28.1',
    ],
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
    ],
    keywords=('notes console terminal'),
)
