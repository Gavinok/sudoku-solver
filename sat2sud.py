#!/usr/bin/env python3

import sys
import operator
import string


def read_input():
    data = []
    for line in sys.stdin:
        # print(line.strip())
        if line == "UNSAT":
            print("Unsatisfiable\n")
        else:
            data.append(line.split())

    data = data[1:]  # removes 'SAT' from list
    # data = ''.join(data)
    # print(data)
    raw_data = []
    for x in data:
        for y in x:
            raw_data.append(y)

    # print(raw_data)
    return raw_data


def make_list(data_input):
    my_list = []

    # breaks a list into a groups of 9
    for i in range(0, len(data_input), 9):
        group = data_input[i : i + 9]
        my_list.append(group)
        # print(group)

    my_list.pop()  # removes final 0 in text file

    rows = 9
    cols = 9
    new_list = []
    count = 0
    for i in range(rows):
        row = []
        for j in range(cols):
            int_list = [
                int(x) for x in my_list[count]
            ]  # converts each element in my_list from sting to int and stores result in int_list
            positive_ints = [
                y for y in int_list if y > 0
            ]  # adds all positive numbers in int_list to list

            num_in_cell = positive_ints[0] % 9

            if num_in_cell == 0:
                num_in_cell = 9
            print(
                "This is: {}, positive no.= {}, and sudoku answer {}\n".format(
                    my_list[count], positive_ints[0], num_in_cell
                )
            )
            # print(num_in_cell)
            # print('\n')
            row.append(num_in_cell)
            count += 1
        new_list.append(row)

    return new_list


def display_sudoku_puzzle(sudoku_puzzle):
    grid = [0, 0, 0]
    count = 0
    for x in sudoku_puzzle:
        for y in range(0, len(x), 3):
            second_group = x[y : y + 3]
            grid[count] = (
                str(second_group[0]) + str(second_group[1]) + str(second_group[2])
            )
            count += 1
        count = 0
        print(grid[0] + " " + grid[1] + " " + grid[2])
        # print('\n')


if __name__ == "__main__":

    data_input = read_input()
    solved_sudoku_puzzle = make_list(data_input)
    display_sudoku_puzzle(solved_sudoku_puzzle)
