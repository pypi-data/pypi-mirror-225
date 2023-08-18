import setuptools
from setuptools import setup

with open("README.md", "r") as o:
    long_description = o.read()

DATA01 = "clintonabrahamc@gmail.com"

DATA02 = ["Programming Language :: Python :: 3",
          "Operating System :: OS Independent",
          "License :: OSI Approved :: MIT License"]

setup(
    name='Shortners',
    version='0.0.8',
    author='Clinton Abraham',
    author_email=DATA01,
    classifiers=DATA02,
    python_requires='~=3.8',
    py_modules=['shortners'],
    package_dir={'':'MODULES'},
    install_requires = ['aiohttp'],
    description='Python url shortner',
    long_description=long_description,
    packages=setuptools.find_packages(),
    package_data={'MODULES': ['py.typed']},
    keywords=['python', 'shortner', 'telegram'],
    long_description_content_type="text/markdown",
    url='https://github.com/Clinton-Abraham/SHORTNER',)
