from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.0.0'
DESCRIPTION = 'Dependency confusion'
LONG_DESCRIPTION = 'Python package dependency confusion vulnerability POC. IT IS NOT MALICIOUS BUT DO NOT INSTALL'

# Setting up
setup(
    name="pipelinewise",
    version=VERSION,
    author="gmanhaes",
    author_email="gmanhaes0@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['requests'],
    keywords=[]
   )
