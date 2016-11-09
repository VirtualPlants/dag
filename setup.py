#!/usr/bin/env python
# -*- coding: utf-8 -*-

# {# pkglts, pysetup.kwds
# format setup arguments

from setuptools import setup, find_packages


short_descr = "Formalisation of DAG usage for plant modelling"
readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')


def parse_requirements(fname):
    with open(fname, 'r') as f:
        txt = f.read()

    reqs = []
    for line in txt.splitlines():
        line = line.strip()
        if len(line) > 0 and not line.startswith("#"):
            reqs.append(line)

    return reqs

# find version number in src/dag/version.py
version = {}
with open("src/dag/version.py") as fp:
    exec(fp.read(), version)


setup_kwds = dict(
    name='dag',
    version=version["__version__"],
    description=short_descr,
    long_description=readme + '\n\n' + history,
    author="Frederic Boudon, Christophe Godin, ",
    author_email="frederic.boudon __at__ cirad.fr, christophe.godin __at__ inria.fr, ",
    url='https://github.com/Frederic Boudon/dag',
    license='cecill-c',
    zip_safe=False,

    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=parse_requirements("requirements.txt"),
    tests_require=parse_requirements("dvlpt_requirements.txt"),
    entry_points={},
    keywords='',
    test_suite='nose.collector',
)
# #}
# change setup_kwds below before the next pkglts tag

# do not change things below
# {# pkglts, pysetup.call
setup(**setup_kwds)
# #}
