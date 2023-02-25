while read l; do
    echo $l | ./sud2sat1 > input.txt
    minisat input.txt out.txt
    ./sat2sud < out.txt
    rm -f input.txt out.txt
done < top95
