all: test

full: main.py ./sat2sud.py
	./main.py > input.txt
	@-minisat input.txt out.txt
	./sat2sud.py < out.txt
	rm -f input.txt out.txt

test: main.py
	./main.py < top95
