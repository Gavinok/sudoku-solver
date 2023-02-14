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


def encodeCell(cell: str) -> SudokuNumber | EmptyCell:
    """Converts a cell into either a list of SudokuNumber (being the
    number at that cell) or a list of EmptyCell indicating nothing was
    found at that cell

    The reason it returns a list of EmptyCell specifically is due to python
    not letting me iterate over Optionals

    """
    if cell == ".":
        return EmptyCell()
    else:
        return SudokuNumber(cell)


def cnfEncodeLine(line: str) -> list[SudokuNumber | EmptyCell]:
    "Convert a line into a list of nu"
    return list(map(encodeCell, line.rstrip()))


def printBaseEncoding(encodedVersion: list[list[SudokuNumber | EmptyCell]]) -> None:
    """Base encoding for every cell contains at least one number"""
    # Iterator used to generate a new number every time next is called
    # on it.
    iter = varGenerator()
    possible_values = 9
    # May have over done it on the list composition here
    base_encoding: list[list[int]] = [
        [next(iter) for _ in range(possible_values)]
        for row in encodedVersion
        for cell in row
    ]

    max_value = next(iter) - 1

    print("c Every cell contains at least one number")
    print(f"p cnf {max_value} {max_value//possible_values}")
    for cell in base_encoding:
        print(" ".join(map(str, cell)) + " 0")


def main():
    # TODO Maybe drop last line if it's not started with a number
    # character
    input = [line for line in stdin]
    encodedVersion = [*map(cnfEncodeLine, input)]
    printBaseEncoding(encodedVersion)


if __name__ == "__main__":
    main()
