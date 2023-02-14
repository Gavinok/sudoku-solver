#!/usr/bin/env python3

from sys import stdin
from itertools import chain


def varGenerator():
    current_var = 0
    while True:
        current_var += 1
        yield current_var


def encodeCell(cell: str) -> list[str] | list[None]:
    if cell == "":
        return [None]
    else:
        return [c for c in cell]


def cnfEncodeLine(line: str) -> list[str | None]:
    return list(chain(*map(encodeCell, line.rstrip().split("."))))


def printBaseEncoding(encodedVersion: list[list[str | None]]):
    # Every cell contains at least one number
    # Iterator used to generate a new number every time next is called on
    # it
    iter = varGenerator()
    possible_values = 9
    base_encoding: list[list[list[str]]] = [
        [[str(next(iter)) for _ in range(possible_values)] + ["0"] for _ in row]
        for row in encodedVersion
    ]

    max_value = next(iter) - 1

    print("c Every cell contains at least one number")
    print(f"p cnf {max_value} {max_value//possible_values}")
    for row in base_encoding:
        for cell in row:
            print(" ".join(cell))


# TODO maybe only drop it if that actually is the case since they may
# not feed us the exact same file
# Drop the last line since it's just the eof character
def main():
    encodedVersion = [*map(cnfEncodeLine, stdin)][0:-1]
    printBaseEncoding(encodedVersion)
