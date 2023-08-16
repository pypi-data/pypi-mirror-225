from argparse import ArgumentParser, Namespace
from csv import DictWriter
import dataclasses
import os

from .converter import lines_to_records
from .record import Record

def parse_args() -> Namespace:
    parser = ArgumentParser(description="Converts exported MLN records to CSV")
    parser.add_argument("files", nargs="+", type=str, help="The list of files to convert")
    return parser.parse_args()


def main():
    """Runs the CLI for `mln_converter`
    :returns: TODO

    """
    fieldnames = [f.name for f in dataclasses.fields(Record)]
    args = parse_args()

    for filename in args.files:
        base_name = os.path.splitext(filename)[0]
        csv_filename = f"{base_name}.csv"
        with open(filename) as fp:
            lines = fp.readlines()
        records = lines_to_records(lines)
        with open(csv_filename, "w", newline="") as fp:
            writer = DictWriter(fp, fieldnames=fieldnames, delimiter="|")
            writer.writeheader()
            writer.writerows(dataclasses.asdict(record) for record in records)
