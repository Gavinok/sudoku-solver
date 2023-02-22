#!/usr/bin/env python3

from sys import stdin
from itertools import chain
from typing import Tuple, Union, List
from typing import TypeVar, Sequence
import math


class SudokuNumber:
    def __init__(self, num: int):
        self.number = num

    def __str__(self) -> str:
        return str(self.number)


class EmptyCell:
    def __str__(self) -> str:
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


def varGenerator():
    """Generates unique numbers from 0 onward infinitely. There is
    probably something built in for this in Python but it's slipping
    my mind"""
    current_var = 0
    while True:
        current_var += 1
        yield current_var


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


def nextMultipleOfSomething(smaller: int, desiredMultiple: int) -> int:
    # written to make expanded tasks easier
    return smaller + (desiredMultiple - (smaller % desiredMultiple))


def nextMultipleOfNine(value: int) -> int:
    # written to make logic easier
    # gets the smallest multiple of nine larger than the input value
    return value + (9 - (value % 9))


def getBaseEncoding(
    encodedVersion: List[List[Union[SudokuNumber, EmptyCell]]]
) -> PuzzleSolution:
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

    return PuzzleSolution(base_encoding, encodedVersion, max_value)


def printBaseEncoding(base_encoding: PuzzleSolution) -> None:
    """Base encoding for every cell contains at least one number"""
    # Iterator used to generate a new number every time next is called
    # on it.
    possible_values = 9
    print("c Every cell contains at least one number")
    print(
        f"p cnf {base_encoding.largest_variable} {base_encoding.largest_variable//possible_values}"
    )
    for cell in base_encoding.current_encoding:
        print(" ".join(map(str, cell)) + " 0")


def printNoDoubleRowEncoding(
    puzzle: PuzzleSolution,
) -> None:
    listOfInputs = puzzle.current_encoding
    puzzleList = puzzle.current_puzzle
    lineCount = 0
    forbiddenValues = set()
    for i, puzzleRow in enumerate(puzzleList):
        for j, puzzleCell in enumerate(puzzleRow):
            if isinstance(puzzleCell, SudokuNumber):
                cellValue = baseNineSingleVal(puzzleCell.number)
                forbiddenValues.add(cellValue)

                # Negate all values that don't match this cell value
                for k, literal in enumerate(listOfInputs[lineCount]):
                    if baseNineSingleVal(literal) != cellValue:
                        listOfInputs[lineCount][k] = -literal
                    else:
                        listOfInputs[lineCount][k] = abs(literal)
                lineCount += 1
            elif isinstance(puzzleCell, EmptyCell):
                print(forbiddenValues)
                literalRow = listOfInputs[lineCount]
                # Not completely sure what this is doing
                for a, literal in enumerate(literalRow):
                    for forbiddenValue in forbiddenValues:
                        if baseNineSingleVal(literal) == forbiddenValue:
                            literalRow[a] = -literal
                lineCount += 1
        # End Of A Row
        if lineCount % 9 == 0:
            forbiddenValues = set()

    maxValues = puzzle.largest_variable
    possible_values = 9
    print("c Every Row contains no duplicate numbers!")
    print(f"p cnf {maxValues} {maxValues//possible_values}")
    on_var = 0
    for cell in listOfInputs:
        on_var += 1
        print(" ".join(map(str, cell)) + " 0")
        if on_var % 9 == 0:
            print("c END OF ROW")


# Cuz I figure this may as well be generic for now
T = TypeVar("T")  # Declare type variable


def transpose(lst: List[List[T]]) -> List[List[T]]:
    return list(map(list, zip(*lst)))


def printNoColEncoding(no_col_dup_encoding: PuzzleSolution) -> None:
    maxValues = no_col_dup_encoding.largest_variable
    possible_values = 9
    print("c Every Column contains no duplicate numbers!")
    print(f"p cnf {maxValues} {maxValues//possible_values}")
    for row in no_col_dup_encoding.current_encoding:
        print(" ".join(map(str, row)) + " 0")


def getNoColEncoding(base_encoding: PuzzleSolution) -> PuzzleSolution:
    base = base_encoding.current_encoding
    # Zip each element of the input encoding with the variables associated with it
    # e.g. [(1 , [ 1 ,2 ,3 ,4 , 5 , 6 , 7 , 8, 9])
    #       (6 , [ 10 , 12 , 13 , 14 , 15 , 16 , 17 , 18, 19])]
    base_with_vars = list(
        map(
            list,
            map(
                zip,
                base_encoding.current_puzzle,
                [base[i : i + 9] for i in range(0, len(base) - 9, 9)],
            ),
        )
    )
    transposed_encoding: List[
        List[Tuple[Union[SudokuNumber, EmptyCell], List[int]]]
    ] = transpose(base_with_vars)

    for row in transposed_encoding:
        print([str(col[0]) + str(col[1]) for col in row])

    lineCount = 0
    forbiddenValues = set()
    new_cell_vals: List[List[int]] = []
    for row in transposed_encoding:
        for puzzleCell in row:
            cell_val = puzzleCell[0]
            cell_vars = puzzleCell[1]
            if isinstance(cell_val, SudokuNumber):
                print("Adding " + str(cell_val))
                current_num = cell_val.number
                forbiddenValues.add(baseNineSingleVal(current_num))
                # Negate all values that don't match this cell value
                new_cell_vals.append(
                    list(
                        map(
                            lambda v: abs(v)
                            if baseNineSingleVal(v) == current_num
                            else -v,
                            cell_vars,
                        )
                    )
                )
                lineCount += 1
            elif isinstance(cell_val, EmptyCell):
                print("Adding " + str(cell_val))
                print(forbiddenValues)
                # Not completely sure what this is doing
                new_cell_vals.append(
                    list(
                        map(
                            lambda v: 0 - v
                            if baseNineSingleVal(v) in forbiddenValues
                            else v,
                            cell_vars,
                        )
                    )
                )
                lineCount += 1
            else:
                raise Exception(
                    "Puzzle Cells must be of type SudokuNumber or EmptyCell but got "
                    + str(cell_val)
                )
        forbiddenValues = set()
    return PuzzleSolution(
        new_cell_vals, base_encoding.current_puzzle, base_encoding.largest_variable
    )


def main():
    # TODO Maybe drop last line if it's not started with a number
    # character
    # input = [line for line in stdin]
    # sideLength = int(math.sqrt(len(input)))

    testInput = "163805070008040065005007008450082039301000040700000000839050000604200590000093081"
    # Now flattens the list into a single line
    no_row_encoding = [
        item for sublist in [*map(cnfEncodeLine, testInput)] for item in sublist
    ]
    # This splits the input into rows of 9
    encoded_with_rows: List[List[Union[SudokuNumber, EmptyCell]]] = [
        no_row_encoding[i : i + 9] for i in range(0, len(no_row_encoding) - 9, 9)
    ]
    for row in encoded_with_rows:
        print([str(col) for col in row])

    print("NOW THE TRANSPOSED VERSION")
    for row in transpose(encoded_with_rows):
        print([str(col) for col in row])

    printBaseEncoding(getBaseEncoding(encoded_with_rows))
    printNoDoubleRowEncoding(getBaseEncoding(encoded_with_rows))
    printNoColEncoding(getNoColEncoding(getBaseEncoding(encoded_with_rows)))


if __name__ == "__main__":
    main()
