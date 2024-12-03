#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import os
import re

# https://adventofcode.com/2024/day/3


def add_multiplications(data):
    regex = re.compile(r'mul\((\d+),(\d+)\)')
    res = 0
    for match in regex.finditer(data):
        res += int(match.group(1)) * int(match.group(2))
    return res

def extract_valid_satements(data):
    # get all the positions of the don't() and do() statements
    dont_regex = re.compile(r'don\'t\(\)')
    do_regex = re.compile(r'do\(\)')
    dont_positions = [match.start() for match in dont_regex.finditer(data)]
    do_positions = [match.start() for match in do_regex.finditer(data)]

    # dontt include the statements if they are preceeded by a don't()
    res = ""
    ok_to_add = True
    for i in range(len(data)):
        if i in dont_positions:
            ok_to_add = False
        if i in do_positions:
            ok_to_add = True
        if ok_to_add:
            res += data[i]
    return res

def add_multiplications_with_conditional_statements(data):
    res = 0
    valid_statements = extract_valid_satements(data)
    #print(valid_statements)
    res = add_multiplications(valid_statements)
    return res

class TestAdventOfCodeDay2(unittest.TestCase):
    def setUp(self):
        """
        Set up test data for unit tests.
        """
        self.data_1 = 'xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))'
        self.data_2 = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"

    def test_add_multiplications(self):
        """
        Test add_multiplications function.
        """
        self.assertEqual(add_multiplications(self.data_1), 161)

    def test_add_multiplications_with_conditional_statements(self):
        """
        Test add_multiplications_with_conditional_statements function.
        """
        self.assertEqual(add_multiplications_with_conditional_statements(self.data_2), 48)


def load_data(input_file):
    # find the rigth data path when called from the root directory or from the src directory
    paths = ['data/' + input_file, '2024/data/' + input_file, '../data/' + input_file]
    for file_name in paths:
        if os.path.exists(file_name):
            break
    if not os.path.exists(file_name):
        raise FileNotFoundError(f"Input file not found: {input_file}")

    with open(file_name, 'r') as f: data = f.read()
    return data

def main():
    input_file = '03.txt'
    data = load_data(input_file)

    print("Multiplications: ", add_multiplications(data))
    print("Multiplications with conditional statements: ", add_multiplications_with_conditional_statements(data))


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # Run tests
        unittest.main(argv=[sys.argv[0]])
    else:
        # Execute the main function
        main()