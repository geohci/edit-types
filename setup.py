from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Edit diffs and type detection for Wikipedia'
LONG_DESCRIPTION = 'A package that allows edit diffs and type detection for Wikipedia.'

# Setting up
setup(
    name="edittypes",
    version=VERSION,
    author="geohci & Amamgbu (Isaac Johnson & Jesse Amamgbu )",
    author_email="<amamgbujesse@yahoo.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['mwparserfromhell', 'anytree'],
    keywords=['python', 'wikipedia', 'edit types', 'edit diffs', 'wiki', 'edit detection'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)