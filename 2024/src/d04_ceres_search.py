#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import os
import re

# https://adventofcode.com/2024/day/4

def load_data(input_file):
    # find the rigth data path when called from the root directory or from the src directory
    data = None
    paths = ['data/' + input_file, '2024/data/' + input_file, '../data/' + input_file]
    for file_name in paths:
        if os.path.exists(file_name):
            break
    if not os.path.exists(file_name):
        raise FileNotFoundError(f"Input file not found: {input_file}")

    with open(file_name, 'r') as f: 
        data = f.read()
    return data

def get_strings_horizontal(data):
    strings = []
    for i in range(len(data)):
        strings.append(''.join(data[i]))
    return strings

def get_strings_vertical(data):
    strings = []
    for i in range(len(data)):
        strings.append(''.join([data[j][i] for j in range(len(data))]))
    return strings

def get_strings_diagonal_top_left_bottom_right(data):
    strings = []
    n = len(data)
    for i in range(n):
        x = i
        y = 0
        s = ''
        while x < n and y < n and x >= 0 and y >= 0:
            s += data[x][y]
            x -= 1
            y += 1
        strings.append(s) if s != "" else None

    for i in range(1, n):
        x = n - 1
        y = i
        s = ''
        while x < n and y < n and x >= 0 and y >= 0:
            s += data[x][y]
            x -= 1
            y += 1
        strings.append(s) if s != "" else None
    return strings

def get_strings_diagonal_top_right_bottom_left(data):
    strings = []
    n = len(data)
    for i in range(n):
        x = i
        y = 0
        s = ''
        while x < n and y < n and x >= 0 and y >= 0:
            s += data[x][y]
            x += 1
            y += 1
        strings.append(s) if s != "" else None

    for i in range(1, n):
        x = 0
        y = i
        s = ''
        while x < n and y < n and x >= 0 and y >= 0:
            s += data[x][y]
            x += 1
            y += 1
        strings.append(s) if s != "" else None
    return strings


def count_string(data, search_string):
    """
    Count the number of occurence of a string in a matrix. 
    The search can be horizontal, vertical or diagonal, in all directions.
    """
    normal_str = search_string
    reversed_str = search_string[::-1]
    count = 0
    strings = get_strings_horizontal(data) + get_strings_vertical(data) + get_strings_diagonal_top_right_bottom_left(data) + get_strings_diagonal_top_left_bottom_right(data)

    # find number of occurences of the search strings
    for s in strings:
        count += s.count(normal_str)
        count += s.count(reversed_str)
    
    return count

class TestAdventOfCodeDay(unittest.TestCase):
    def setUp(self):
        """
        Set up test data for unit tests.
        """

        self.test_data = [
            list("MMMSXXMASM"),
            list("MSAMXMSMSA"),
            list("AMXSXMAAMM"),
            list("MSAMASMSMX"),
            list("XMASAMXAMM"),
            list("XXAMMXXAMA"),
            list("SMSMSASXSS"),
            list("SAXAMASAAA"),
            list("MAMMMXMMMM"),
            list("MXMXAXMASX")
        ]

        self.test_data_numeric = [
            list("0123456789"),
            list("0123456789"),
            list("0123456789"),
            list("0123456789"),
            list("0123456789"),
            list("0123456789"),
            list("0123456789"),
            list("0123456789"),
            list("0123456789"),
            list("0123456789")
        ]
    def test_count_string(self):
        """
        Test count_string function.
        """
        self.assertEqual(count_string(self.test_data, "XMAS"), 18)
 
    def test_load_data(self):
        """
        Test load_data function.
        """
        self.assertIsNotNone(load_data('04.txt'))


def main():
    input_file = '04.txt'
    data = load_data(input_file)
    print(data[1])

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # Run tests
        unittest.main(argv=[sys.argv[0]])
    else:
        # Execute the main function
        main()