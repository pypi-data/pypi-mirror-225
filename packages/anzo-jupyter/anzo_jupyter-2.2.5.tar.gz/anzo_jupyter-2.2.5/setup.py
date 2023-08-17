#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

#with open('HISTORY.md') as history_file:
    #history = history_file.read()
history = ""

requirements = []

setup_requirements = []

test_requirements = []

setup(
    author="Tommy Fang, Adam Sachs, Alex Ledger",
    author_email='',
    python_requires='>=3.5',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Anzo-Jupyter is a Jupyter Extension for interacting with Anzo in Jupyter",
    entry_points={
        'console_scripts': [],
    },
    install_requires=requirements,
    long_description=readme + '\n\n' + history,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords='anzo_jupyter',
    name='anzo_jupyter',
    packages=find_packages(include=['anzo_jupyter', 'anzo_jupyter.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='',
    version='2.2.5',
    zip_safe=False,
)
