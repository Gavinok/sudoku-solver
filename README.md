# Group Members
- Gavin Jaeger-Freeborn (V00849637)
- AJ ... (V00...)
- Ian Weber (V00...)

# Contents Of Repo
- sat2sud.py
  - source code for `sat2sud`
- sud2sat.py
  - source code for `sud2sat`
- p096_sudoku.txt 
  - The test input found https://projecteuler.net/project/resources/p096_sudoku.txt
- testinput.txt 
  - A single sudoku puzzle from p096_sudoku used for testing.
  - see Makefile for example usage
- testharness.py
  - Source code to benchmark `sud2sat` against p096_sudoku.txt
- Makefile
  - Makefile to test `sud2sat` and `sat2sud` as well as produce the
    executables themselves

# Build

To produce the final `sud2sat` and `sat2sud` executable run

```bash
make
```

# Running

To test the sud2sat and sat2sud run the following commands (after building the project)

```bash
./sud2sat < testinput.txt > input.txt
@-minisat input.txt out.txt
./sat2sud < out.txt
rm -f input.txt out.txt
```

# Development Setup (only necessary if you are not running on UVic's server)
Install `poetry` and `pyenv`g

Install Virtual Environment
```bash
pyenv install 3.8.10
pyenv local 3.8.10
```

Configure poetry to use it
```bash
poetry env use python3.8
poetry install
```

Start a shell with everything good to go
```bash
poetry shell
python -V
```
