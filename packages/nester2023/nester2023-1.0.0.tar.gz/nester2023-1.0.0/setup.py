# This file contains metadata about your distribution.


from distutils.core import setup

# read the contents of your README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# name, version , py_modules, autor, author_email.... are the setup function's arguments


setup(
    name            ='nester2023',
    version         ='1.0.0',
    py_modules      =['nester'],  # Associate your module's (nester.py) metadata with the setup functions arguments.
    author          ='SM',
    author_email    ='sonalimetkar1@gmail.com',
    description     ='A simple printer of nested lists',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='',
    install_requires=[],
)
