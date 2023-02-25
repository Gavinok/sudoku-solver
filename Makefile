all: benchmark

full: main.py ./sat2sud.py
	./main.py < testinput.txt > input.txt
	@-minisat input.txt out.txt
	./sat2sud.py < out.txt
	rm -f input.txt out.txt

benchmark: main.py sat2sud.py testharness.py
	./testharness.py < p096_sudoku.txt

executables: main.py sat2sud.py
	cp ./main.py ./sud2sat
	cp ./sat2sud.py ./sat2sud
