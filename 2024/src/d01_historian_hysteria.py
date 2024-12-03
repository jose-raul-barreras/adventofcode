#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

# https://adventofcode.com/2024/day/1


def total_distance(left_list, right_list):
    res = 0
    # unique values
    left_sorted = sorted(left_list)
    right_sorted = sorted(right_list)

    # min length
    min_len = min(len(left_sorted), len(right_sorted))

    # total distance
    for i in range(min_len):
        res += abs(left_sorted[i] - right_sorted[i])

    return res

def similarity_score(left_list, right_list):
    res = 0
    for left_element in left_list:
        count = 0
        for right_element in right_list:
            if left_element == right_element:
                count += 1
        res += left_element * count
    return res

class TestAdventOfCodeDay1(unittest.TestCase):
    def setUp(self):
        """
        Set up test data for unit tests.
        """
        self.left_list = [3, 4, 2, 1, 3, 3]
        self.right_list = [4, 3, 5, 3, 9, 3]

    def test_total_distance(self):
        """
        Test total_distance function.
        """
        self.assertEqual(total_distance(self.left_list, self.right_list), 11)

    def test_similarity_score(self):
        """
        Test similarity_score function.
        """
        left_list = [3, 4, 2, 1, 3, 3]
        right_list = [4, 3, 5, 3, 9, 3]
        self.assertEqual(similarity_score(self.left_list, self.right_list), 31)

def main():
    file_name = '../data/01.txt'
    left_list = []
    right_list = []
    i = 0
    with open(file_name, 'r') as f: input = f.read().split("\n")
    for data in input:
        left_list.append(int(data.split()[0]))
        right_list.append(int(data.split()[1]))

    print("Total distance: ", total_distance(left_list, right_list))
    print("Similarity score: ", similarity_score(left_list, right_list))

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # Run tests
        unittest.main(argv=[sys.argv[0]])
    else:
        # Execute the main function
        main()