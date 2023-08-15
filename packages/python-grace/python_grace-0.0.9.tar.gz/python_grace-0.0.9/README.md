python-grace
============

[![Test](https://github.com/tueda/python-grace/workflows/Test/badge.svg?branch=main)](https://github.com/tueda/python-grace/actions?query=branch:main)
[![PyPI version](https://badge.fury.io/py/python-grace.svg)](https://pypi.org/project/python-grace/)

An unofficial Python wrapper for [the GRACE system](https://minami-home.kek.jp/)
(the public version for tree-level computations).

*This is a pre-alpha version.*


Requirements
------------

- Python >= 3.6.1
- pip >= 19.0
- C compiler
- Fortran compiler
- Make utility
- X Window system (optional, for `gracefig` and `grcdraw`)
- Motif Toolkit or its clone (optional, for `gracefig`)
- `ps2pdf` in Ghostscript (optional, to generate PDF files with `gracefig`)

**Debian or Ubuntu**

```sh
sudo apt-get install gfortran ghostscript libmotif-dev make python3-pip
```

**Fedora**

```sh
sudo dnf install gcc-gfortran ghostscript make motif-devel python3-pip
```


Installation
------------

Use [`pip`](https://pip.pypa.io/):
```sh
pip install python-grace
```
which installs the `grace` command.
(You may need to adjust `$PATH`.
You can always use `python -m grace`, instead.)

To select the compilers, specify them as environment variables when `pip` runs:
```sh
CC=gcc-12 FC=gfortran-12 pip install python-grace
```

You can use [`pipx`](https://pypa.github.io/pipx/) instead of `pip`
if you prefer to install this software in an isolated and/or temporary environment.


Example
-------

```sh
mkdir my_process
cd my_process
grace template sm/eewwa
grace grc
grace gracefig - # requires optional dependencies
grace grcfort
make all
./gauge
./integ
./spring
```


Development
-----------
```sh
poetry install
poetry run task prepare
```


License
-------

The code in this repository is covered under
[the MIT license](https://github.com/tueda/python-grace/blob/main/LICENSE).

Note that, however, the source code of the GRACE system is *not* MIT licensed.
Indeed, this repository itself does not contain any part of GRACE.
When you install this software, the source code distribution of GRACE will
automatically be downloaded from the original site.
