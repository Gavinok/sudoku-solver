#!/usr/bin/env python3
from sys import stdin
import subprocess


input = [line for line in stdin]
tests = [input[i : i + 9] for i in range(1, len(input), 10)]
for test in tests:
    p = subprocess.run(
        ["./sud2sat"],
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
    with open("output.txt", "r") as text_file:
        p2 = subprocess.run(
            ["./sat2sud"],
            stdout=subprocess.PIPE,
            input=text_file.read(),
            encoding="ascii",
        )
        print(p2.stdout)
