import os
import re
from setuptools import setup


# Utility function to read the README file.
def read(file):
    return open(os.path.join(os.path.dirname(__file__), file)).read()


def get_version():
    version_file = 'monitoring/_version.py'
    version_str = read(version_file).strip()
    version_re = r"^__version__ = ['\"]([^'\"]*)['\"]"
    mo = re.search(version_re, version_str, re.M)
    if mo:
        version = mo.group(1)
    else:
        raise RuntimeError("Unable to find version string in %s." % (version_file,))
    return version


def get_install_requires():
    res = list()
    res.append('pyyaml>=3.10')
    res.append('voluptuous>=0.9.3')
    return res


setup(
    name='pymonitor',
    version=get_version(),
    author="Colin Carleton",
    author_email="colin.m.carleton@gmail.com",
    description="Lightweight python monitoring",
    keywords="monitoring",
    url="https://github.com/colincarleton/PyMonitor",
    packages=['pymonitor'],
    long_description=read('README.rst'),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: System Administrators',
        'Operating System :: POSIX :: Linux',
        'Topic :: System :: Monitoring',
    ],
)
