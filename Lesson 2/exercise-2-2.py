#!/usr/bin/env python3

import sys
#print sys.argv
from itertools import repeat

def bitStrings(number):
	bit_String = list(repeat(0, number))
	bit_String_end = list(repeat(1, number))
	print(bit_String)
	print(bit_String_end)

	test = [0,1,2,3]
	print(test)
	test.reverse()
	print(test)


	bit_String.reverse()
	indices_zero = [i for i, x in enumerate(bit_String) if x == 0] #find all indices of 0 in the list bit_String
	min_index = min(indices_zero)
	if min_index == 0:
		bit_String[0] = 1

	else:
		
	for index in indices_zero:

		pass
	#while (bit_String != bit_String_end):

	#	pass

print("Hej python3")
arguments = sys.argv[1:]
print(arguments)

for argument in arguments:
	print("Run binary")
	bitStrings(int(argument))


