import os

from distutils.core import setup

setup(
    name='pin-pip',
    version='0.1',
    packages=['pin.plugins'],
    author="Dustin Lacewell",
    author_email="dlacewell@gmail.com",
    url="https://github.com/dustinlacewell/pin-pip",
    description="Plugins providing basic pip functionality for pin.",
    long_description=open('README.markdown').read(),
)
