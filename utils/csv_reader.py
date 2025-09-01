import csv
from pathlib import Path


def csv_reader(path):
    file_path = Path(__file__).resolve().parent.parent / path
    with open(file_path, newline="", encoding="utf-8") as f:
        csv_rows = csv.reader(f)
        next(csv_rows, None)  # skip header
        return [tuple(row) for row in csv_rows]





