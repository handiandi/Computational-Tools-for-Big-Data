#!/bin/bash
# using awk, we can take each line and find the fifth column (price) using $5 and compare with 10000 our threshold
awk '($5 < 10000)' cars.txt
