import csv
import sys
from typing import Generator


def read_csv(
    fname: str = "/home/work/fastapi/web_fastapi/src/db/creature.psv", num: int = 5
):
    with open(fname) as f:
        for row in range(num):
            yield next(csv.reader(f, delimiter="|"))


if __name__ == "__main__":
    for row in read_csv():
        print(row)
