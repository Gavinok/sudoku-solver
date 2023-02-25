all: sud2sat sat2sud

target: sud2sat sat2sud

sud2sat: sud2sat.py
	cp ./sud2sat.py ./sud2sat
sat2sud: sat2sud.py
	cp ./sat2sud.py ./sat2sud

full: sud2sat sat2sud
	./sud2sat < testinput.txt > input.txt
	@-minisat input.txt out.txt
	./sat2sud < out.txt
	rm -f input.txt out.txt

benchmark: sud2sat sat2sud testharness.py
	./testharness.py < p096_sudoku.txt

clean:
	rm -f sud2sat sat2sud
