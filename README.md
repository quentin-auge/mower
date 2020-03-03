# Lawn mowers technical test

The code runs with Python >= 3.6. It does not have any production
dependency, relying exclusively on standard library.  
It is locally pip-installable, exposing a `mower` command line tool,
complete with debug mode.  
Internal libraries powering the project are fully tested
(coverage = 100%).

It is an implementation of a company's technical test.  
For this reason, instructions are not linked nor explicited.
Anonymity is key.

## Setup

* Clone the repository:
  ```
  git clone https://github.com/quentin-auge/mower.git
  ```

* Move into the directory:
  ```
  cd mower/
  ```

* (Optional) Create a virtual environment and activate it:
  ```
  virtualenv -p python3 .venv
  source .venv/bin/activate
  ```

* Install the application inside the virtualenv
  ```
  pip install .
  ```

## Run the application

To aggregate the provided [instructions file](sample_input.txt):
```
$ cat ./sample_input.txt
5 5
1 2 N
LFLFLFLFF
3 3 E
FFRFFRFRRF

$ mower ./sample_input.txt
1 3 N
5 1 E
```

Debug mode:
```
$ mower -v ./sample_input.txt
DEBUG:mower.cli: Parsed grid size: (5, 5)
DEBUG:mower.cli: Parsed mowers: ['1 2 N', '3 3 E']
DEBUG:mower.cli: Parsed moves: ['LFLFLFLFF', 'FFRFFRFRRF']
DEBUG:mower.cli:
DEBUG:mower.cli: Mower 1
DEBUG:mower.cli:   1 2 N
DEBUG:mower.cli: L 1 2 W
DEBUG:mower.cli: F 0 2 W
DEBUG:mower.cli: L 0 2 S
DEBUG:mower.cli: F 0 1 S
DEBUG:mower.cli: L 0 1 E
DEBUG:mower.cli: F 1 1 E
DEBUG:mower.cli: L 1 1 N
DEBUG:mower.cli: F 1 2 N
DEBUG:mower.cli: F 1 3 N
DEBUG:mower.cli:
DEBUG:mower.cli: Mower 2
DEBUG:mower.cli:   3 3 E
DEBUG:mower.cli: F 4 3 E
DEBUG:mower.cli: F 5 3 E
DEBUG:mower.cli: R 5 3 S
DEBUG:mower.cli: F 5 2 S
DEBUG:mower.cli: F 5 1 S
DEBUG:mower.cli: R 5 1 W
DEBUG:mower.cli: F 4 1 W
DEBUG:mower.cli: R 4 1 N
DEBUG:mower.cli: R 4 1 E
DEBUG:mower.cli: F 5 1 E
DEBUG:mower.cli:
1 3 N
5 1 E
```

Usage:
```
$ mower --help
usage: mower [-h] [--verbose] path

Move mowers on a lawn

positional arguments:
  path           instructions file for moving the mowers on the lawn

optional arguments:
  -h, --help     show this help message and exit
  --verbose, -v  debug_mode
```

## Run the tests

Install `tox` and run it:
```
pip install tox
tox
```

Tox outputs the (branch) coverage at the end.
