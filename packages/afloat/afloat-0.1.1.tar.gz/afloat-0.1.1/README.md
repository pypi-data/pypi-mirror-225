<!-- # <img src="./sphinx/goatafloat.jpg" width="100"> **AFLOAT**  -->
# <img src="./sphinx/goatafloat.jpg" width="400">  
## (**A** **F**airly useful **L**ibrary of **O**cean **A**nalysis **T**ools)

[![Documentation status](https://readthedocs.org/projects/afloat/badge/?version=latest)](https://gptide.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/afloat.svg)](https://badge.fury.io/py/afloat)
[![Downloads](https://pepy.tech/badge/afloat)](https://pepy.tech/project/afloat)

A collection of basic utilities to giving a quick interface to data analysis tools in numpy and scipy, often through xarray. Key elements: 
- Simplification of working with time data
- Logical API rather than a dump of modules
- Use of xarray accessors 
- Pip installable through pipy

## Documentation
The documentation can be found [here](https://iosonobert.github.io/afloat/).

## Config file
For full functionality you'll need a .afloatcongig file in your home directory [USERPROFILE directory in Windows]. The file should contain:

afloat-extras: <path to afloat-extras folder>

## Other names:
- **B**asic **O**cean **A**nalysis **T**ools [BOAT Taken on pypi]
- **G**eneral **O**cean **A**nalysis **T**ools [GOAT Taken on pypi]
- **B**asic **E**nvironmental **A**nalysis **T**ools [BEAT Taken on pypi]

<!-- ![alt text](./doc/unlicensed_goat.jpg) -->
<!-- ![alt text](./sphinx/goatafloat.jpg) -->

## History:
This package is built on the code of numerous other open access libraries. Major sources:
- mrayson/sfoda
- iosonobert/sfoda
- iosonobert/pIMOS
- iosonobert/turbo_tools
- mrayson/oceanmooring 
- mrayson/iwaves 
- iosonobert/zutils
- lkilcher/dolfyn
- iosonobert/dolfyn
- iosonobert/dallsporpoise

## Interactive; Slow.  
This is NOT designed to run quickly. It has does a lot of data conversion during function calls etc. It is designed to simplify hacking around in interactively. 
