from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.1.0'
DESCRIPTION = 'Edit diffs and type detection for Wikipedia'
LONG_DESCRIPTION = 'A package that allows edit diffs and type detection for Wikipedia.'

# Dev dependencies
EXTRAS_REQUIRE = {
    "tests": ["pytest>=6.2.5"],
}

EXTRAS_REQUIRE["dev"] = (
    EXTRAS_REQUIRE["tests"]
)

# Setting up
setup(
    name="mwedittypes",
    version=VERSION,
    author="geohci & Amamgbu (Isaac Johnson & Jesse Amamgbu)",
    author_email="<amamgbujesse@yahoo.com>",
    url="https://github.com/geohci/edit-types",
    license="MIT License",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['mwparserfromhell', 'anytree'],
    keywords=['python', 'wikipedia', 'edit types', 'edit diffs', 'wiki', 'edit detection'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        
    ],
    extras_require=EXTRAS_REQUIRE,
    include_package_data=True,
    zip_safe=False,
)