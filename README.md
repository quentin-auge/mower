# Mower technical test

The code runs with Python >= 3.6.

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

Usage:
```
$ mower --help
usage: mower [-h] path

Move a mower around

positional arguments:
  path        instructions file for moving the mower

optional arguments:
  -h, --help  show this help message and exit
```

## Run the tests

Install `tox` and run it:
```
pip install tox
tox
```

Tox outputs the coverage at the end.

Get more details about the coverage after running tox:
```
cd tests/
coverage html
```

The HTML report can then be found at `htmlcov/index.html`.
