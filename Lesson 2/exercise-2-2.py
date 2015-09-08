#!/usr/bin/env python3

import sys
#print sys.argv
from itertools import repeat

def bitStrings(number):
	bit_String = list(repeat(0, number))
	bit_String_end = list(repeat(1, number))
	print(bit_String)
	print(bit_String_end)

	#while (bit_String != bit_String_end):

	#	pass

print("Hej python3")
arguments = sys.argv[1:]
print(arguments)

for argument in arguments:
	print("Run binary")
	bitStrings(int(argument))


