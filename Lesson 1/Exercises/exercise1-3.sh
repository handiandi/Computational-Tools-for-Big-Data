#!/bin/bash
if [ $# -eq 2 ]
  then
    grep -E '\w+' -o $1 | sort | awk '{print tolower($0)}' | uniq | comm -23 - <(sort $2)
elif [ $# -eq 1 ]
  then
    grep -E '\w+' -o $1 | sort | awk '{print tolower($0)}' | uniq | comm -23 - <(sort dict.txt)
else
    echo "Too few or too many input"
fi