#!/bin/bash

total=0
failed=0

for testcase in *.tex; do
    name=$(basename $testcase)

    echo "Testing $name..."

    ../dlatex.py $testcase json > $name.out

    if [ $# -eq 1 ] && [ $1 = 'define' ]; then
        cp $name.out $name.expected
    fi

    if ! cmp -s $name.out $name.expected; then
        ((failed += 1))
        diff -y $name.out $name.expected
    else
        rm $name.out
    fi

    ((total += 1))
done

echo "Cleaning up..."

rm *.aux *.log *.pdf

passed=$((total - failed))

echo ""
echo "Complete! $passed/$total tests passed"