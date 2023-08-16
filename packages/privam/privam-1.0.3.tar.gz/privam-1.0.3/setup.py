from setuptools import setup, find_packages

with open('README.md', 'r') as readme_file:
    long_description = readme_file.read()

setup(
    name='privam',
    version='1.0.3',
    packages=find_packages(),
    install_requires=['python-socketio'],
    long_description=long_description,
    long_description_content_type='text/markdown',  # Specify the content type
)