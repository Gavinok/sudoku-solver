#!/usr/bin/env python3

from sys import stdin
from itertools import chain
from typing import Union, List
import math

class SudokuNumber:
    def __init__(self, num: int):
        self.number_string = num

    def __str__(self) -> int:
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
    if (number % 9 > 0):
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

def getBaseEncoding(encodedVersion: List[List[Union[SudokuNumber, EmptyCell]]]) -> None:
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

    printNoDoubleRowEncoding(base_encoding, encodedVersion, max_value)
        

def printBaseEncoding(encodedVersion: List[List[Union[SudokuNumber, EmptyCell]]]) -> None:
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
    possible_values = 9
    print("c Every cell contains at least one number")
    print(f"p cnf {max_value} {max_value//possible_values}")
    for cell in base_encoding:
        print(" ".join(map(str, cell)) + " 0")


def printNoDoubleRowEncoding(listOfInputs: List[List[int]], puzzleList: List[List[Union[SudokuNumber, EmptyCell]]], maxValues: int) -> None:
    i = -1
    for puzzleRow in puzzleList:
        #initialize list of values that may not be repeated
        forbiddenValues = []
        i = i + 1
        for puzzleCell in puzzleRow:
            if isinstance(puzzleCell, SudokuNumber):
                ##This doesn't seem to work correctly.
                ##It SHOULD set all non-matching literals in a given list to negative if the value is set
                print("This cell has a value!")
                for literal in listOfInputs[i]:
                    print(baseNineSingleVal(literal), puzzleCell.number_string)
                    if baseNineSingleVal(literal) != puzzleCell.number_string:
                        literal = -literal
                        forbiddenValues.append(puzzleCell.number_string)
            else:
                print("No match")
                #  if there are literals that are on the unacceptable list, the values should be negated
                if baseNineSingleVal(literal) in forbiddenValues:
                    literal = -literal

    possible_values = 9
    print("c Every Row contains no duplicate numbers!")
    print(f"p cnf {maxValues} {maxValues//possible_values}")
    for cell in listOfInputs:
        print(" ".join(map(str, cell)) + " 0")
    
"""
def getNoDoubleRowEncoding(listOfInputs: List[List[int]], puzzleList: List[List[Union[SudokuNumber, EmptyCell]]]) -> List[List[int]]:
    for literalRow, puzzleCellRow in zip(listOfInputs, puzzleList):
        for literal, puzzleCell in zip(literalRow, puzzleCellRow):
            forbiddenValues = []
            if isinstance(puzzleCell, SudokuNumber):
                for value in literal:
                    if baseNineSingleVal(value) != int(puzzleCell.number_string):
                        value = -value
                        forbiddenValues.append(puzzleCell.number_string)
            else:
                for value in literal:
                    if baseNineSingleVal(value) in forbiddenValues:
                        value = -value
    return listOfInputs
"""                    
            
        
        

def main():
    # TODO Maybe drop last line if it's not started with a number
    # character
    #input = [line for line in stdin]
    #sideLength = int(math.sqrt(len(input)))

    testInput = "163805070008040065005007008450082039301000040700000000839050000604200590000093081"
    encodedVersion = [*map(cnfEncodeLine, testInput)]
    printBaseEncoding(encodedVersion)
    getBaseEncoding(encodedVersion)

if __name__ == "__main__":
    main()
