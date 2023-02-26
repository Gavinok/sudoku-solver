#!/usr/bin/env python3
import io
import time
from os import times
from sys import stdin
from functools import reduce
import subprocess


def benchmark(sud2satexe):
    results = []
    with open("p096_sudoku.txt", "r") as sudfile:
        input = [line for line in sudfile.readlines()]
        tests = [input[i : i + 9] for i in range(1, len(input), 10)]
        for test in tests:
            p = subprocess.run(
                [sud2satexe],
                stdout=subprocess.PIPE,
                input="".join(test),
                encoding="ascii",
            )
            with open("input.txt", "w") as text_file:
                text_file.write(p.stdout)
                p = subprocess.run(
                    ["minisat", "input.txt", "output.txt"],
                    stdout=subprocess.PIPE,
                    encoding="ascii",
                )
            results.append(
                [
                    float(line.split(": ")[1].split(" ")[0])
                    for line in p.stdout.splitlines()
                    if line.startswith("C") or line.startswith("M")
                ]
            )
            time.sleep(1)

    memres = list(map(lambda x: x[0], results))
    cpures = list(map(lambda x: x[1], results))

    print("Results for " + sud2satexe)
    print("results are" + str(results))
    print("mem average are " + str(reduce(lambda a, b: a + b, memres) / len(results)))
    print("mem worst are " + str(reduce(max, memres)))
    print(
        "cpu time average are " + str(reduce(lambda a, b: a + b, cpures) / len(results))
    )
    print("cpu time average are " + str(max(cpures)))


benchmark("./sud2sat")
time.sleep(2)
benchmark("./sud2sat1")
time.sleep(2)
benchmark("./sud2sat2")
time.sleep(2)
benchmark("./sud2sat3")
