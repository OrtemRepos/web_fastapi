import pandas as pd
import sys


def read_csv(fname: str) -> list[tuple]:
    data = pd.read_csv(fname, sep="|")
    return data


if __name__ == "__main__":
    data = read_csv(sys.argv[1])
    print(data.head(5))
