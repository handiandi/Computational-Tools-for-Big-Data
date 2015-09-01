#!/bin/bash
grep -E "\w+" -o $1 | sort | uniq -c | sort -nr | head -10

