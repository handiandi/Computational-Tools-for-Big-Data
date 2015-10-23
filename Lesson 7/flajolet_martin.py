#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import mmh3
import bitarray
import re
import statistics
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

class FlajoletMartinCounter():
    """
    Implementation of Flajolet Martin Algorithm
    for aproximating distinct objects in a streaming dataset
    """
    def __init__(self, integer_bits = 32, seed = 0):
        self.integer_bits = integer_bits
        self.hash_seed = seed
        self.array = bitarray.bitarray(integer_bits)
        self.array.setall(0)
    
    def trailing_zeroes(self, num):
        """Counts the number of trailing 0 bits in num."""
        if num == 0:
            return 32 # Assumes 32 bit integer inputs!
        p = 0
        while (num >> p) & 1 == 0:
            p += 1
        return p
    
    def process(self, element):
        """
        process an element by hashing it in the range 0:2^32-1
        and use number of trailing zeroes as index
        """
        index = self.trailing_zeroes(mmh3.hash(element, seed=self.hash_seed) % (2**self.integer_bits)-1)
        self.array[index] = 1

    def give_estimate(self):
        """
        estimate cardinality as 2^R/corr_factor
        """
        r_index = 0
        while(self.array[r_index] != 0 and r_index < self.integer_bits-1):
            r_index += 1
        return (2**r_index) / 0.77351

def extract_text(string):
    lowered = string.lower().strip()
    return re.split("\W+", lowered)

if __name__ == '__main__':
    plot_list = []
    with open("shakespeare.txt") as f:
        shakespeare_words = extract_text(f.read())
    actual_number_of_words = len(set(shakespeare_words))

    for x in range(1,30):
        K = x
        L = x
        counter_list = []
        for i in range(K*L):
            counter_list.append(FlajoletMartinCounter(seed=i))

        for word in shakespeare_words:
            for counter in counter_list:
                counter.process(word)
    
        mean_vals = []
        for i in range(K):
            mean_vals.append(statistics.median([counter.give_estimate() for counter in counter_list[L*i:L*(i+1)]]))

        plot_list.append((x,statistics.mean(mean_vals)))

    plt.title("Flajolet Martin with different K and L values")
    plt.plot(*zip(*plot_list), color="red")
    plt.ylabel("number of elements")
    plt.xlabel("values for K and L")
    
    red_patch = mpatches.Patch(color="red", label="approximations")
    blue_patch = mpatches.Patch(color="blue", label="actual elements")
    plt.legend(handles=[red_patch,blue_patch])
    
    plt.axhline(y=actual_number_of_words, color="blue")
    plt.legend()
    plt.show()
    print("K and L level of 5 approximates: {} with an actual number of words being: {}".format(plot_list[4],actual_number_of_words))
