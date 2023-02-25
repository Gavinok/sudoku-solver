all: executables

full: sud2sat.py ./sat2sud.py
	./sud2sat.py < testinput.txt > input.txt
	@-minisat input.txt out.txt
	./sat2sud.py < out.txt
	rm -f input.txt out.txt

benchmark: sud2sat.py sat2sud.py testharness.py
	./testharness.py < p096_sudoku.txt

executables: sud2sat.py sat2sud.py
	cp ./sud2sat.py ./sud2sat
	cp ./sat2sud.py ./sat2sud
