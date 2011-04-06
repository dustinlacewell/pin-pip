import os

from distutils.core import setup

setup(
    name='pin-pip',
    version='0.2',
    packages=['pin.plugins'],
    requires=["pip", "pin"],
    author="Dustin Lacewell",
    author_email="dlacewell@gmail.com",
    url="https://github.com/dustinlacewell/pin-pip",
    description="Plugins providing basic pip functionality for pin.",
    long_description=open('README.markdown').read(),
)
