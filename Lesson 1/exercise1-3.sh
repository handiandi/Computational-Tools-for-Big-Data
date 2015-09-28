#!/bin/bash
# we use grep with -E flag and regex "\w+" to get all words and -o flag to get each on a separate output line
# sort to make duplicate entries consecutive and awk converting all to lowercase
# uniq to remove consecutive duplicates
# comm to compare the files, however the files both need to be sorted
# to sort the dict and make it appear as a file we use process substitution
if [ $# -eq 2 ]
  then
    grep -E '\w+' -o $1 | sort | awk '{print tolower($0)}' | uniq | comm -23 - <(sort $2)
elif [ $# -eq 1 ]
  then
    grep -E '\w+' -o $1 | sort | awk '{print tolower($0)}' | uniq | comm -23 - <(sort dict.txt)
else
    echo "Too few or too many input"
fi
