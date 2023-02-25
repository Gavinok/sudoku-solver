#!/usr/bin/env python3

from itertools import count
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
    iter = count(1)
    possible_values = 9
    # May have over done it on the list composition here
    base_encoding: list[list[int]] = [
        [next(iter) for _ in range(possible_values)]
        for row in encodedVersion
        for cell in row
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


def printBaseEncoding(base_encoding: PuzzleSolution) -> None:
    """Base encoding for every cell contains at least one number"""
    # Iterator used to generate a new number every time next is called
    # on it.
    possible_values = 9
    base_rules = noDupInRow()
    base_rules2 = noDupInCol()
    base_rules3 = noDupIn3x3()
    print(
        f"p cnf {base_encoding.largest_variable} {(len(base_encoding.current_encoding)) + len(base_rules) + len(base_rules2) + len(base_rules3)}"
    )
    for cell in base_rules:
        print(" ".join(map(str, cell)) + " 0")
    for cell in base_rules2:
        print(" ".join(map(str, cell)) + " 0")
    for cell in base_rules3:
        print(" ".join(map(str, cell)) + " 0")
    print("c Every cell contains at least one number")
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
                # print(forbiddenValues)
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


def removeDuplicates(
    p: List[List[Tuple[Union[SudokuNumber, EmptyCell], List[int]]]]
) -> List[List[int]]:

    lineCount = 0
    forbiddenValues = set()
    new_cell_vals: List[List[int]] = []
    for row in p:
        for puzzleCell in row:
            cell_val = puzzleCell[0]
            cell_vars = puzzleCell[1]
            if isinstance(cell_val, SudokuNumber):
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
                # Not completely sure what this is doing
                new_cell_vals.append(
                    list(
                        map(
                            lambda v: -v
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
    return new_cell_vals


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
                [base[i : i + 9] for i in range(0, len(base), 9)],
            ),
        )
    )
    transposed_encoding: List[
        List[Tuple[Union[SudokuNumber, EmptyCell], List[int]]]
    ] = transpose(base_with_vars)
    new_cell_vals = removeDuplicates(transposed_encoding)
    return PuzzleSolution(
        new_cell_vals, base_encoding.current_puzzle, base_encoding.largest_variable
    )


class SudokuNumberVarsPair:
    """Dedicated class for the combination of a suduko number and the
    associated list of variables"""

    def __init__(
        self, sudoku_number: Union[SudokuNumber, EmptyCell], sat_vars: List[int]
    ):
        self.sudoku_number = sudoku_number
        self.sat_vars = sat_vars

    def __repr__(self) -> str:
        if isinstance(self.sudoku_number, SudokuNumber):
            return "(" + str(self.sudoku_number.number) + "," + str(self.sat_vars) + ")"
        else:
            return "(" + str(self.sudoku_number) + "," + str(self.sat_vars) + ")"

    def __str__(self) -> str:
        if isinstance(self.sudoku_number, SudokuNumber):
            return "(" + str(self.sudoku_number.number) + "," + str(self.sat_vars) + ")"
        else:
            return "(" + str(self.sudoku_number) + "," + str(self.sat_vars) + ")"


class ThreeByThree:
    """A class used to describe a block of 3x3 SudokuNumberVarsPair"""

    def __init__(self, row1, row2, row3) -> None:
        assert len(row1) == 3
        assert len(row2) == 3
        assert len(row3) == 3
        self.row = row1 + row2 + row3

    def __repr__(self) -> str:
        return "3x3(" + str(self.row) + ")"


def getNo3x3Dup(base_encoding: PuzzleSolution) -> PuzzleSolution:
    base = base_encoding.current_encoding
    # Zip each element of the input encoding with the variables associated with it
    # e.g. [(1 , [ 1 ,2 ,3 ,4 , 5 , 6 , 7 , 8, 9])
    #       (6 , [ 10 , 12 , 13 , 14 , 15 , 16 , 17 , 18, 19])]
    base_with_vars = list(
        map(
            list,
            map(
                # lambda x, y: map(SudokuNumberVarsPair, x, y),
                zip,
                base_encoding.current_puzzle,
                [base[i : i + 9] for i in range(0, len(base), 9)],
            ),
        )
    )
    # split each row into blocks of 3
    blocks_of_3 = list(
        map(
            lambda row: [
                [row[i + 0], row[i + 1], row[i + 2]] for i in range(0, len(row), 3)
            ],
            base_with_vars,
        )
    )
    # This is kinda cursed but it splits the rows into blocks of 3
    blocks_of_3x3: List[ThreeByThree] = [
        num
        for elem in [
            [
                ThreeByThree(
                    blocks_of_3[i][0], blocks_of_3[i + 1][0], blocks_of_3[i + 2][0]
                ),
                ThreeByThree(
                    blocks_of_3[i][1], blocks_of_3[i + 1][1], blocks_of_3[i + 2][1]
                ),
                ThreeByThree(
                    blocks_of_3[i][2], blocks_of_3[i + 1][2], blocks_of_3[i + 2][2]
                ),
            ]
            for i in range(0, len(blocks_of_3), 3)
        ]
        for num in elem
    ]

    new_cell_vals = removeDuplicates(list(map(lambda b: b.row, blocks_of_3x3)))

    return PuzzleSolution(
        new_cell_vals, base_encoding.current_puzzle, base_encoding.largest_variable
    )


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


def test():
    testInput = "163805070008040065005007008450082039301000040700000000839050000604200590000093081"
    # Now flattens the list into a single line
    no_row_encoding = [
        item for sublist in [*map(cnfEncodeLine, testInput)] for item in sublist
    ]
    # This splits the input into rows of 9
    encoded_with_rows: List[List[Union[SudokuNumber, EmptyCell]]] = [
        no_row_encoding[i : i + 9] for i in range(0, len(no_row_encoding), 9)
    ]
    print("block of 3")
    getNo3x3Dup(getBaseEncoding(encoded_with_rows))


def printEncoding(puz: PuzzleSolution, comment: str) -> None:
    maxValues = puz.largest_variable
    possible_values = 9
    print("c " + comment)
    print(f"p cnf {maxValues} {maxValues//possible_values}")
    for row in puz.current_encoding:
        print(" ".join(map(str, row)) + " 0")


def encode_board(b: PuzzleSolution) -> PuzzleSolution:
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
    clauses = []
    for i in range(1, 10):
        for k in range(1, 10):
            for j in range(1, 10):
                for l in range(j + 1, 10):
                    clauses.append(
                        [
                            -((81 * (i - 1)) + (9 * (j - 1)) + (k - 1) + 1),
                            -((81 * (i - 1)) + (9 * (l - 1)) + (k - 1) + 1),
                        ]
                    )
    return clauses


def noDupInCol():
    clauses = []
    for j in range(1, 10):
        for k in range(1, 10):
            for i in range(1, 10):
                for l in range(i + 1, 10):
                    clauses.append(
                        [
                            -((81 * (i - 1)) + (9 * (j - 1)) + (k - 1) + 1),
                            -((81 * (l - 1)) + (9 * (j - 1)) + (k - 1) + 1),
                        ]
                    )
    return clauses


def noDupIn3x3():
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


def main():
    # TODO Maybe drop last line if it's not started with a number
    # character
    # input = [line for line in stdin]
    # sideLength = int(math.sqrt(len(input)))

    testInput = "163805070008040065005007008450082039301000040700000000839050000604200590000093081"

    encoded_with_rows: List[List[Union[SudokuNumber, EmptyCell]]] = encodeAsRows(
        testInput
    )

    printBaseEncoding(getBaseEncoding(encoded_with_rows))

    # printNoDoubleRowEncoding(getBaseEncoding(encoded_with_rows))
    # printEncoding(
    #     getNoColEncoding(getBaseEncoding(encoded_with_rows)),
    #     "Every Column contains no duplicate numbers!",
    # )
    # printEncoding(
    #     getNo3x3Dup(getBaseEncoding(encoded_with_rows)), "No duplicates in a 3x3 block"
    # )
    # base_encoding = getBaseEncoding(encoded_with_rows)
    # print(
    #     list(
    #         map(
    #             list,
    #             map(
    #                 # lambda x, y: map(SudokuNumberVarsPair, x, y),
    #                 zip,
    #                 base_encoding.current_puzzle,
    #                 [
    #                     base_encoding.current_encoding[i : i + 9]
    #                     for i in range(0, len(base_encoding.current_encoding), 9)
    #                 ],
    #             ),
    #         )
    #     )
    # )


def noColDup2(maxValues):
    return [
        [-(x), -(x + (9 * y))]
        for x in range(1, (maxValues))
        for y in range(baseNineSingleVal(x), 8)
    ]


if __name__ == "__main__":
    main()
