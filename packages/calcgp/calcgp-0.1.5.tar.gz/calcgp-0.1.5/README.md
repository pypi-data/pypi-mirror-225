# CalcGP: Numerical Calculus via Gaussian Process Regression

 1. [ Introduction ](#introduction)
 2. [ Installation ](#installation)

## Introduction
CalcGP is a Gaussian Process Regression framework built as an alternative for numerical integration of gradients and differentiation of scalar functions. The package is based on the autograd framework [JAX](https://github.com/google/jax). 

CalcGP is intended to be used as a regression framework for scalar functions and gradients of scalar functions. One can
- directly fit a scalar function from observations,
- "integrate" the gradient of a scalar function,
- "differentiate" a scalar function in order to get its gradient.

Examples for all these cases can be found in `./examples/`. There is a 1D example that shows all three use cases, a 2D example on how to handle higher dimensional data, and an example that shows a sparse model for large datasets.

## Installation

Download the package from github via

```shell
git clone https://github.com/LukasEin/calcgp.git
```

Then, to install the package directly, run

```shell
python3 setup.py install --user
```

or to install it in a conda environment run

```shell
conda create -n myenv python=3.8
conda activate myenv
python3 setup.py install
```

direcly in the newly created `./calcgp/` folder.