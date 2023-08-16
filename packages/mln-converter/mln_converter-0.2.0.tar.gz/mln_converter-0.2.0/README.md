# Minuteman Library Network (MLN) Record Converter

Historical loan records exported via the [MLN website](https://minlib.net) are in a semi-human
readable format, making them difficult to use in analyses. This utility converts each record into a
`Record` object that can be inspected in multiple ways.

## Dev install

### Prerequisites

* [Python 3.10+](https://www.python.org/downloads/)
* [Poetry for Python](https://python-poetry.org/docs/)

### Installation

Clone the git repository locally and run `poetry install` from the main directory. On Ubuntu:

```bash
git clone git@gitlab.com:woodforsheep/mln-to-csv.git
cd mln-to-csv
poetry install
```

## Command Line Use

```bash
poetry run mln-to-csv --help
Using python3 (3.11.4)
usage: mln-to-csv [-h] files [files ...]

Converts exported MLN records to CSV

positional arguments:
  files       The list of files to convert

options:
  -h, --help  show this help message and exit

```

## Library use

The main utility in the library is `lines_to_records` and can be used as follows:

```Python
from mln_converter import lines_to_records

with open(records_file) as fp:
    lines = fp.readlines()
records = lines_to_records(lines)

for record in records:
    print(f"{record.titles[0]} ({record.authors[0]})")
```

<a href="https://www.flaticon.com/free-icons/convert" title="convert icons">Convert icons created by iconsax - Flaticon</a>
