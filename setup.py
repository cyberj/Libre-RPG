import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "libre-rpg",
    version = "0.0.1",
    author = "Johan Charpentier",
    author_email = "cyberj@arcagenis.org",
    description = ("Yet another open RPG engine"),
    license = "GPLv3",
    keywords = "rpg",
    url = "http://github.com/cyberj/libre-rpg",
    packages=['libreprg', 'tests'],
    long_description=read('README.rst'),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Games/Entertainment :: Role-Playing",
        "License :: OSI Approved :: GNU General Public License (GPL)",
    ],
)

