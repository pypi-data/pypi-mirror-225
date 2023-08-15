# fmath

A library for Python for fast math on floats

See the [demo](https://github.com/donno2048/fmath/blob/master/test.ipynb)

## Installation

### From PyPI

```sh
pip3 install fmath
```

### From GitHub

```sh
pip3 install git+https://github.com/donno2048/fmath
```

## Usage

Just replace

```py
from math import sqrt
pow = pow
abs = abs
sign = lambda x: x >= 0
```

with

```py
from fmath import sqrt, pow, abs, sign
```

and make sure the input is `float`
