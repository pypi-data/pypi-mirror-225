import os
import re
import setuptools

NAME = "privapy"
AUTHOR = "Vincent Min"
AUTHOR_EMAIL = "vincentmin17@gmail.com"
DESCRIPTION = "Anonymize your data"
LICENSE = "MIT License"
KEYWORDS = "anonymize"
URL = "https://github.com/vincentmin/" + NAME
README = ".github/README.md"
CLASSIFIERS = [
    "Development Status :: 2 - Pre-Alpha",
    "Intended Audience :: Developers",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "License :: OSI Approved :: MIT License",
]
INSTALL_REQUIRES = [
    "transformers==4.31.0",
    "torch==2.0.1",
    "opencv-python==4.8.0.76",
    "pillow",
    "timm",
]
ENTRY_POINTS = {}
SCRIPTS = []

HERE = os.path.dirname(__file__)


def read(file):
    with open(os.path.join(HERE, file), "r") as fh:
        return fh.read()


VERSION = re.search(
    r'__version__ = [\'"]([^\'"]*)[\'"]', read(NAME.replace("-", "_") + "/__init__.py")
).group(1)

LONG_DESCRIPTION = read(README)

if __name__ == "__main__":
    setuptools.setup(
        name=NAME,
        version=VERSION,
        packages=setuptools.find_packages(),
        author=AUTHOR,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type="text/markdown",
        license=LICENSE,
        keywords=KEYWORDS,
        url=URL,
        classifiers=CLASSIFIERS,
        install_requires=INSTALL_REQUIRES,
        entry_points=ENTRY_POINTS,
        scripts=SCRIPTS,
        include_package_data=True,
    )
