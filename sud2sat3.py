#!/usr/bin/env python3

from itertools import count
from sys import stdin
from typing import Tuple, Union, List


class SudokuNumber:
    def __init__(self, num: int):
        self.number = num

    def __str__(self) -> str:
        return str(self.number)

    def __repr__(self) -> str:
        return str(self.number)


class EmptyCell:
    def __str__(self) -> str:
        return "EmptyCell"

    def __repr__(self) -> str:
        return "EmptyCell"


BaseEncoding = List[List[int]]


class PuzzleSolution:
    def __init__(
        self,
        current_encoding: BaseEncoding,
        current_puzzle: List[List[Union[SudokuNumber, EmptyCell]]],
        largest_variable: int,
    ) -> None:
        self.current_encoding = current_encoding
        self.current_puzzle = current_puzzle
        self.largest_variable = largest_variable


def encodeCell(cell: str) -> Union[SudokuNumber, EmptyCell]:
    """Converts a cell into either a list of SudokuNumber (being the
    number at that cell) or a list of EmptyCell indicating nothing was
    found at that cell

    The reason it returns a list of EmptyCell specifically is due to python
    not letting me iterate over Optionals

    """
    if cell == "." or cell == "*" or cell == "0" or cell == "?":
        return EmptyCell()
    else:
        return SudokuNumber(int(cell))


def cnfEncodeLine(line: str) -> List[Union[SudokuNumber, EmptyCell]]:

    "Convert a line into a list of nu"
    return list(map(encodeCell, line.rstrip()))


def baseNineSingleVal(number: int) -> int:
    if number % 9 > 0:
        return number % 9
    else:
        return 9


def getBaseEncoding(
    encodedVersion: List[List[Union[SudokuNumber, EmptyCell]]]
) -> PuzzleSolution:
    """Base encoding for every cell contains at least one number"""
    # Iterator used to generate a new number every time next is called
    # on it.
    iter = count(1)
    possible_values = 9
    # May have over done it on the list composition here
    base_encoding: list[list[int]] = [
        [next(iter) for _ in range(possible_values)]
        for row in encodedVersion
        for _ in row
    ]
    max_value = next(iter) - 1

    return PuzzleSolution(
        encode_board(
            PuzzleSolution(base_encoding, encodedVersion, max_value)
        ).current_encoding
        + base_encoding,
        encodedVersion,
        max_value,
    )


def printMinimalEncoding(base_encoding: PuzzleSolution) -> None:
    """Produce the minimal encoding for every cell"""
    # Iterator used to generate a new number every time next is called
    # on it.
    rows = noDupInRow()
    columns = noDupInCol()
    three_x_three = noDupIn3x3()
    one_num_per_cell = mostOneNumberInCell()
    every_num_in_row = everyNumAppearsOnceInRow()
    every_num_in_col = everyNumAppearsOnceInCol()
    every_num_in_3x3 = everyNumAppearsInSubgrid()
    print(
        f"p cnf {base_encoding.largest_variable} {len(base_encoding.current_encoding + rows + columns + three_x_three + one_num_per_cell + every_num_in_row + every_num_in_col+ every_num_in_3x3)}"
    )
    print("c Each number appears at most once in every row")
    for cell in rows:
        print(" ".join(map(str, cell)) + " 0")
    print("c Each number appears at most once in every column")
    for cell in columns:
        print(" ".join(map(str, cell)) + " 0")
    print("c Each number appears at most one in every 3x3 sub-grid")
    for cell in three_x_three:
        print(" ".join(map(str, cell)) + " 0")
    print("c Every cell contains at least one number")
    for cell in base_encoding.current_encoding:
        print(" ".join(map(str, cell)) + " 0")
    print("c ---BEGINNING EXTENDED ENCODINGS---")
    print("c There is at most one number in each cel")
    for cell in one_num_per_cell:
        print(" ".join(map(str, cell)) + " 0")


def printOriginalSud(sud: List[List[Union[SudokuNumber, EmptyCell]]]):
    for row in sud:
        print(" ".join([repr(i) if isinstance(i, SudokuNumber) else "0" for i in row]))


def encodeAsRows(text):
    # Now flattens the list into a single line
    no_row_encoding = [
        item for sublist in [*map(cnfEncodeLine, text)] for item in sublist
    ]
    # This splits the input into rows of 9
    encoded_with_rows: List[List[Union[SudokuNumber, EmptyCell]]] = [
        no_row_encoding[i : i + 9] for i in range(0, len(no_row_encoding), 9)
    ]

    return encoded_with_rows


def encode_board(b: PuzzleSolution) -> PuzzleSolution:
    "Encodes te board into a format that can be output indicating the current state of all filled cells"
    base = b.current_encoding
    # Zip each element of the input encoding with the variables associated with it
    # e.g. [(1 , [ 1 ,2 ,3 ,4 , 5 , 6 , 7 , 8, 9])
    #       (6 , [ 10 , 12 , 13 , 14 , 15 , 16 , 17 , 18, 19])]
    base_with_vars: List[List[Tuple[Union[SudokuNumber, EmptyCell], List[int]]]] = list(
        map(
            list,
            map(
                zip,
                b.current_puzzle,
                [base[i : i + 9] for i in range(0, len(base), 9)],
            ),
        )
    )

    return PuzzleSolution(
        [
            [-x] if baseNineSingleVal(x) != cell[0].number else [x]
            for row in base_with_vars
            for cell in row
            if isinstance(cell[0], SudokuNumber)
            for x in cell[1]
        ],
        b.current_puzzle,
        b.largest_variable,
    )


def noDupInRow():
    "Each number appears at most once in every row"
    clauses = []
    for i in range(1, 10):
        for k in range(1, 10):
            for j in range(1, 9):
                for l in range(j + 1, 10):
                    clauses.append(
                        [
                            -((81 * (i - 1)) + (9 * (j - 1)) + (k - 1) + 1),
                            -((81 * (i - 1)) + (9 * (l - 1)) + (k - 1) + 1),
                        ]
                    )
    return clauses


def noDupInCol():
    "Each number appears at most once in every column"
    clauses = []
    for j in range(1, 10):
        for k in range(1, 10):
            for i in range(1, 9):
                for l in range(i + 1, 10):
                    clauses.append(
                        [
                            -((81 * (i - 1)) + (9 * (j - 1)) + (k - 1) + 1),
                            -((81 * (l - 1)) + (9 * (j - 1)) + (k - 1) + 1),
                        ]
                    )
    return clauses


def noDupIn3x3():
    "Each number appears at most one in every 3x3 sub-grid"
    clauses = []
    for k in range(1, 10):
        for a in range(0, 3):
            for b in range(0, 3):
                for u in range(1, 4):
                    for v in range(1, 3):
                        for w in range(v + 1, 4):
                            clauses.append(
                                [
                                    -(
                                        (81 * (((3 * a) + u) - 1))
                                        + (9 * (((3 * b) + v) - 1))
                                        + (k - 1)
                                        + 1
                                    ),
                                    -(
                                        (81 * (((3 * a) + u) - 1))
                                        + (9 * (((3 * b) + w) - 1))
                                        + (k - 1)
                                        + 1
                                    ),
                                ]
                            )

    for k in range(1, 10):
        for a in range(0, 3):
            for b in range(0, 3):
                for u in range(1, 3):
                    for v in range(1, 4):
                        for w in range(u + 1, 4):
                            for t in range(1, 4):
                                clauses.append(
                                    [
                                        -(
                                            (81 * (((3 * a) + u) - 1))
                                            + (9 * (((3 * b) + v) - 1))
                                            + (k - 1)
                                            + 1
                                        ),
                                        -(
                                            (81 * (((3 * a) + w) - 1))
                                            + (9 * (((3 * b) + t) - 1))
                                            + (k - 1)
                                            + 1
                                        ),
                                    ]
                                )

    return clauses


def mostOneNumberInCell():
    "There is at most one number in each cell"
    clauses = []
    for i in range(1, 10):
        for j in range(1, 10):
            for k in range(1, 9):
                for l in range(k + 1, 10):
                    clauses.append(
                        [
                            -((81 * (i - 1)) + (9 * (j - 1)) + (k - 1) + 1),
                            -((81 * (i - 1)) + (9 * (j - 1)) + (l - 1) + 1),
                        ]
                    )
    return clauses


def everyNumAppearsOnceInRow():
    "There is at most one number in each cell"
    clauses = []
    for i in range(1, 10):
        for k in range(1, 10):
            clauses.append(
                [((81 * (i - 1)) + (9 * (j - 1)) + (k - 1) + 1) for j in range(1, 10)]
            )
    return clauses


def everyNumAppearsOnceInCol():
    "There is at most one number in each cell"
    clauses = []
    for j in range(1, 10):
        for k in range(1, 10):
            clauses.append(
                [((81 * (i - 1)) + (9 * (j - 1)) + (k - 1) + 1) for i in range(1, 10)]
            )
    return clauses


def everyNumAppearsInSubgrid():
    "Each number appears at most one in every 3x3 sub-grid"
    clauses = []
    for k in range(1, 10):
        for a in range(0, 3):
            for b in range(0, 3):
                clauses.append(
                    [
                        (
                            (81 * (((3 * a) + u) - 1))
                            + (9 * (((3 * b) + v) - 1))
                            + (k - 1)
                            + 1
                        )
                        for u in range(1, 4)
                        for v in range(1, 4)
                    ]
                )

    return clauses


def demo():
    testInput = "163805070008040065005007008450082039301000040700000000839050000604200590000093081"

    encoded_with_rows: List[List[Union[SudokuNumber, EmptyCell]]] = encodeAsRows(
        testInput
    )

    printMinimalEncoding(getBaseEncoding(encoded_with_rows))


def main():
    # TODO Maybe drop last line if it's not started with a number
    # character
    input = [line for line in stdin]
    encoded_with_rows: List[List[Union[SudokuNumber, EmptyCell]]] = encodeAsRows(input)
    printMinimalEncoding(getBaseEncoding(encoded_with_rows))


if __name__ == "__main__":
    main()
