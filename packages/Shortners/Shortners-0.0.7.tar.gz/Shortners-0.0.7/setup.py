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
    version='0.0.7',
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
    keywords=['python', 'shortner', 'telegram'],
    url='https://github.com/DC4-WARRIOR/SHORTER',
    long_description_content_type="text/markdown",)
