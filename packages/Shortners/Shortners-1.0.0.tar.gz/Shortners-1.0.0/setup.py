from setuptools import setup, find_packages

with open("README.md", "r") as o:
    long_description = o.read()

DATA01 = "clintonabrahamc@gmail.com"

DATA02 = ["Programming Language :: Python :: 3",
          "Operating System :: OS Independent",
          "License :: OSI Approved :: MIT License"]

setup(
    name='Shortners',
    version='1.0.0',
    author='Clinton Abraham',
    author_email=DATA01,
    classifiers=DATA02,
    zip_safe=False,
    python_requires='~=3.8',
    packages=find_packages(),
    install_requires=['aiohttp'],
    description='Python url shortner',
    long_description=long_description,
    keywords=['python', 'shortner', 'telegram'],
    long_description_content_type="text/markdown",
    url='https://github.com/Clinton-Abraham/SHORTNER',)
