#!/bin/bash

# grep with regex \w+ for finding all words and printing on separate lines
# sort for doing initial sort of words (repeated lines required by uniq)
# uniq -c for prefixing with number of occurences using repeated lines
# sort -nr for sorting number of occurences with numeric sort and reversing order to highest first
# head -10 for take the first 10 lines
grep -E "\w+" -o $1 | sort | uniq -c | sort -nr | head -10

