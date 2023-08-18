# privapy

> Anonymize your data

[![Latest Version on PyPI](https://img.shields.io/pypi/v/privapy.svg)](https://pypi.python.org/pypi/privapy/)
[![Supported Implementations](https://img.shields.io/pypi/pyversions/privapy.svg)](https://pypi.python.org/pypi/privapy/)
[![Build Status](https://github.com/vincentmin/privapy/actions/workflows/test.yaml/badge.svg)](https://github.com/vincentmin/privapy/actions/workflows/test.yaml)
[![Documentation Status](https://readthedocs.org/projects/privapy/badge/?version=latest)](https://privapy.readthedocs.io/en/latest/?badge=latest)
[![Coverage Status](https://coveralls.io/repos/github/vincentmin/privapy/badge.svg?branch=main)](https://coveralls.io/github/vincentmin/privapy?branch=main)
[![Built with PyPi Template](https://img.shields.io/badge/PyPi_Template-v0.2.0-blue.svg)](https://github.com/christophevg/pypi-template)

## Documentation

Visit [Read the Docs](https://privapy.readthedocs.org) for the full documentation, including overviews and several examples.

## Installation

```bash
pip install privapy
```

## Disclaimer

This package provides no guarantee of anonymity. It is the user's responsibility to ensure that the data is properly anonymized. The authors of this package are not responsible for any results or misuse of this package.

## Usage

### text

```python
from privapy.text import TextCleaner

text = "I live in New York and work at Google. My email is john@google.com"
cleaner = TextCleaner(steps="all")
cleaned_text = cleaner.clean(text)
# 'I live in <<ENT>> and work at <<ENT>. My email is <<EMAIL>>'
```

### image

```python
from privapy.image import ImageCleaner
from PIL import Image

cleaner = ImageCleaner()
img = Image.open("image.jpg")
cleaned_image = cleaner.clean(img)
```

input image (`img`):
![input image](../docs/_static/input.png)
output image (`cleaned_image`):
![output image](../docs/_static/output.png)

## Coming in future releases

- text
  - Add more cleaning methods
  - Add Spacy integration
- image
  - Add more cleaning methods
    - blackout
    - pixelate
  - Add more detection methods
    - face detection
    - dlib
    - mediapipe
