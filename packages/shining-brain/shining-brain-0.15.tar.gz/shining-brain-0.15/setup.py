"""
This is the build script for setuptools. It provides information about your package such as the 
name, version, description, etc.
"""
from setuptools import setup, find_packages

setup(
    name='shining-brain',
    version='0.15',
    description='Making decisions by analyzing data',
    packages=find_packages(where='src'),
    author='Evan Knox Thomas',
    author_email='evanknoxthomas@gmail.com',
    package_dir={'': 'src'},
    install_requires=['pandas', 'sqlalchemy', 'PyYAML']
)
