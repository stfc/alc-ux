<div align="center">
    <img src="images/alc-100.png" alt="ALC Logo" style="width: 40%">
</div>

# AiiDAlab ALC Application 

![Release](https://img.shields.io/badge/Release-none-red)
[![PyPI Version](https://img.shields.io/badge/PyPI-none-red)](https://pypi.org/)
[![Pipeline Status](https://github.com/stfc/alc-ux/actions/workflows/ci-testing.yml/badge.svg?branch=main)](https://github.com/stfc/alc-ux/actions)
![Coverage Status](https://img.shields.io/badge/Coverage-none-red)
[![Docs status](https://img.shields.io/badge/docs-sphinx-blue)](https://stfc.github.io/alc-ux/)
[![DOI](badge)](https://zenodo.org/)

# My Awesome Project

This is a description of my project.

This is an AiiDAlab application for scientific workflows maintained by the [Ada Lovelace Center](https://adalovelacecentre.ac.uk/) (ALC). 
The app is still in early development stage and any input/contributions are welcome. 


## For Developers 

### Style Checking

This package uses pre-commit hooks to check for style consistency, to use these the ``pre-commit`` tool is required.
This can be installed alongside the base package by running, 

``` sh 
pip install .[dev]
```

or separately via, 

``` sh 
pip install pre-commit 
``` 

Once installed run, 

``` sh 
pre-commit install 
``` 

in the base repository to enable the pre-commit hooks. 
This will now run style and formatting checks on every commit. 

### Testing 

This package uses [pytest](https://docs.pytest.org/en/stable/) 
to run all unit tests which is included in the ```[dev]``` optional 
package dependencies. Once installed it can be run from the project root directory. 
The CI workflows are configured to ensure all tests pass 
before a pull request can be accepted into the main repository.
It is important that any new additions to the code base are accompanied 
by appropriate testing, maintaining a high code coverage. The coverage 
can be checked via, 

``` sh 
pytest --cov=aiidalab_alc 
``` 


### Documentation 

The documentation, including a User Guide, Developer Guide and an API reference, 
is built using [sphinx](https://www.sphinx-doc.org/). The source 
for which is contained in the ```docs/``` directory. At present 
only the html generator has been fully tested. All required packages can 
be installed alongside the core package via, 

``` sh 
pip install .[docs]
```

and then the documentation can be built using sphinx-build, 

``` sh 
sphinx-build -b html docs/source/ docs/build/html 
```

from the root directory. 
