<p align="center">
<img src="./media/logo.jpg" width="700">
</p>

[![PyPI Version](https://img.shields.io/pypi/v/GQCConstraints.svg)](https://pypi.python.org/pypi/GQCConstraints)
[![docs](https://img.shields.io/badge/docs-latest-5077AB.svg?logo=read%20the%20docs)](https://gqcg-res.github.io/GQCConstraints/)
[![Examples](https://img.shields.io/badge/tutorials-green.svg)](/examples/README.md)

# GQCConstraints
GQCConstraints or GQCC for short is a python library, based on [GQCP](https://github.com/GQCG/GQCP), that can be used to run several constrained quantum chemical calculations.

Constraint and symmetries are closely related and as such, applying different kind of constraints on quantum chemical calculations can lead to some very interesting insights. 

# Getting started
In order to get started you first of all need a working `GQCP docker container`.

First [install Docker](https://docs.docker.com/get-docker/). Then pull our `GQCP` image to the infrastructure in question.

```bash
docker pull gqcg/gqcp
```

Next, on top of this installation you can install GQCConstraints.

```bash
pip install GQCConstraints
```

To use the code import both GQCPy and GQCConstraints.

```python
import gqcpy
import GQCC
```

## Reasearch

GQCC is a research tool first and foremost. And research for which this library is used can be found here.

- [Constraining chemical wavefunctions](https://github.com/GQCG-res/constraining_chemical_wave_functions)
- [Constrained entanglement](https://github.com/GQCG-res/constrained-entanglement)
- [Constrained NOCI](https://github.com/GQCG-res/constrained-NOCI)
- [Fukui Hubbard](https://github.com/GQCG-res/fukui-hubbard)
- [Spin contamination constraints](https://github.com/GQCG-res/spin-contamination-constraints)