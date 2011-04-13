import os

from setuptools import setup

setup(
    name='pinpip',
    version='0.1rc1',
    packages=['pin', 'pin.plugins'],
    namespace_packages=['pin', 'pin.plugins'],
    provides=["pinpip"],
    author="Dustin Lacewell",
    author_email="dlacewell@gmail.com",
    url="https://github.com/dustinlacewell/pin-pip",
    description="Plugins providing basic pip functionality for pin.",
    long_description=open('README.markdown').read(),
)
