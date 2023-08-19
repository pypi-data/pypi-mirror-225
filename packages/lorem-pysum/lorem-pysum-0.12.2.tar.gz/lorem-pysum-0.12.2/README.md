<!--suppress HtmlDeprecatedAttribute -->
<div align=center>
  <h1>Lorem Pysum</h1>
  <h3>Library to generate instances of Pydantic models..</h3>
  <img src="https://img.shields.io/badge/License-MIT-blue.svg"
   height="20"
   alt="License: MIT">
  <img src="https://img.shields.io/badge/code%20style-black-000000.svg"
   height="20"
   alt="Code style: black">
  <img src="https://img.shields.io/pypi/v/lorem-pysum.svg"
   height="20"
   alt="PyPI version">
  <img src="https://img.shields.io/badge/coverage-100%25-success"
   height="20"
   alt="Code Coverage">
</div>

## Install

Lorem Pysum is on PyPI and can be installed with:

```shell
poetry add lorem-pysum
```

or

```shell
pip install lorem-pysum
```

## Usage

Given a Pydantic model type Lorem Pysum can generate instances of that model with
randomly generated values.

## Example

```python
from enum import auto, Enum
from uuid import UUID

import lorem_pysum
from pydantic import BaseModel


class Flavor(Enum):
    MOCHA = auto()
    VANILLA = auto()


class Brand(BaseModel):
    brand_name: str


class Coffee(BaseModel):
    id: UUID
    description: str
    cream: bool
    sweetener: int
    flavor: Flavor
    brand: Brand


lorem_pysum.generate(Coffee)
# Result -> id=UUID('550342d5-13ce-4ee1-b73d-d3c5e81607ce') description='string' cream=True sweetener=0 flavor=<Flavor.MOCHA: 1> brand=Brand(brand_name='string')
```
