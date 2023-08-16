# setup.py
from setuptools import setup, find_packages

setup(
    name='privam',
    version='1.0.0',
    packages=find_packages(),
    install_requires=['python-socketio'],  # Add other dependencies here
)
