===========================================
BubbleDet
===========================================

Computes the one-loop functional determinant entering the bubble nucleation
rate, or vacuum decay rate.

|

Requirements
===========================================

Based on Python 3. For necessary dependencies, see `pyproject.toml`.

|


Installation
===========================================

Can be installed as a package with pip, or pip3, using::

    pip install -e .

from the base directory of the repository. To install also optional dependencies
for the docs and tests, instead run::

    pip install -e .[docs,tests]

|

Tests
===========================================

Tests can be run with::

    pytest -v

|

Examples
===========================================

A number of examples are collected in the directory `examples/`, include a
simple real scalar model, a comparison to analytic results in the thin-wall
limit. After installing the package, these can be run directly with Python, as
in::

    python3 examples/first_example.py
