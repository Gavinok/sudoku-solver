#!/usr/bin/env python3

from sys import stdin
from itertools import chain


class SudokuNumber:
    def __init__(self, num: str):
        self.number_string = num

    def __str__(self) -> str:
        return self.number_string


class EmptyCell:
    def __str__(self) -> str:
        return "EmptyCell"


def varGenerator():
    """Generates unique numbers from 0 onward infinitely. There is
    probably something built in for this in Python but it's slipping
    my mind"""
    current_var = 0
    while True:
        current_var += 1
        yield current_var


def encodeCell(cell: str) -> list[SudokuNumber] | list[EmptyCell]:
    """Converts a cell into either a list of SudokuNumber (being the
    number at that cell) or a list of EmptyCell indicating nothing was
    found at that cell

    The reason it returns a list of EmptyCell specifically is due to python
    not letting me iterate over Optionals

    """
    if cell == "":
        return [EmptyCell()]
    else:
        return [SudokuNumber(c) for c in cell]


def cnfEncodeLine(line: str) -> list[SudokuNumber | EmptyCell]:
    "Convert a line into a list of nu"
    return list(chain(*map(encodeCell, line.rstrip().split("."))))


def printBaseEncoding(encodedVersion: list[list[SudokuNumber | EmptyCell]]) -> None:
    """Base encoding for every cell contains at least one number"""
    # Iterator used to generate a new number every time next is called
    # on it.
    iter = varGenerator()
    possible_values = 9
    # May have over done it on the list composition here
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


def main():
    # TODO maybe only drop it if that actually is the case since they may
    # not feed us the exact same file
    # Drop the last line since it's just the eof character
    input = [line for line in stdin][0:-1]
    encodedVersion = [*map(cnfEncodeLine, input)]
    printBaseEncoding(encodedVersion)


if __name__ == "__main__":
    main()
