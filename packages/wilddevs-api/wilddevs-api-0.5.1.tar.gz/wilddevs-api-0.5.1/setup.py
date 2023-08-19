from setuptools import setup, find_packages
import codecs
import os

from wild_devs_api.__version__ import __version__

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

# Setting up
setup(
    name="wilddevs-api",
    version=__version__,
    author="Labret",
    description='A Python API wrapper for the WildDevsAPI',
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['requests', 'aiohttp'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)