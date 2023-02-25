all: sud2sat sat2sud sud2sat1 sud2sat2 sud2sat3

target: all

# Base executables
sud2sat: sud2sat.py
	cp ./sud2sat.py ./sud2sat
sat2sud: sat2sud.py
	cp ./sat2sud.py ./sat2sud

# Extended
sud2sat1: sud2sat.py # This one is already supported
	cp ./sud2sat.py ./sud2sat1
sud2sat2: sud2sat2.py
	cp ./sud2sat2.py ./sud2sat2
sud2sat3: sud2sat3.py
	cp ./sud2sat3.py ./sud2sat3

# Basic test for the default sud2sat
full: all
	./sud2sat2 < testinput.txt > input.txt
	@-minisat input.txt out.txt
	./sat2sud < out.txt
	./sud2sat3 < testinput.txt > input.txt
	@-minisat input.txt out.txt
	./sat2sud < out.txt
	./sud2sat < testinput.txt > input.txt
	@-minisat input.txt out.txt
	./sat2sud < out.txt
	rm -f input.txt out.txt

# Benchmark against all p096_sudoku sudoku inputs
benchmark: sud2sat sat2sud testharness.py
	./testharness.py < p096_sudoku.txt

# Run the top95 tests
top95: sud2sat1 sat2sud
	./runtop95.sh
	rm -f input.txt out.txt

clean:
	rm -f sud2sat sud2sat1 sud2sat2 sud2sat3 sat2sud v00849637.tar.gz

tar: clean
	mkdir -p v00849637
	cp sud2sat.py sud2sat2.py sud2sat3.py sat2sud.py p096_sudoku.txt top95 testinput.txt testharness.py Makefile README.md v00849637/
	tar cvzf v00849637.tar.gz v00849637
