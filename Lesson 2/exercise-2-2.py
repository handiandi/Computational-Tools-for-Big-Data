#!/usr/bin/env python3

"""
	Create a list of list of bit strings of the input value

	:param number: The number which all bit strings should be found
    :return bit_strings: List of all bit strings as lists
"""
def bit_strings(number):
	bit_string = list(repeat(0, number)) #Start bit string, eg. [0, 0, 0]
	bit_string_end = list(repeat(1, number)) #End bit string, eg. [1, 1, 1]

	bit_strings = []
	bit_strings.append(bit_string[:])
	while (bit_string != bit_string_end):
		bit_string.reverse() #Reverse the order of elements in list
		indices_zero = [i for i, x in enumerate(bit_string) if x == 0] #find all indices of 0 in the list bit_String
		min_index = min(indices_zero)
		if min_index == 0: #There is a zero at index 0
			bit_string[0] = 1 #Set the zero to one!

		else:
			for index in range(0,min_index+1):
				if bit_string[index] == 0:
					bit_string[index] = 1
				else:
					bit_string[index] = 0
		bit_string.reverse() #Reverse the order of elements in list (back to original order)
		bit_strings.append(bit_string[:]) #Append all elements by value, not reference! 
	
	return bit_strings




import sys
from itertools import repeat

arguments = sys.argv[1:]

for argument in arguments:
	print("Run binary")
	result = bit_strings(int(argument))
	print("Bit strings for {0}: \n {1}\n\n".format(argument, result))
