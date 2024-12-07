#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import unittest
import copy

# https://adventofcode.com/2024/day/7

# Define paths outside the function to improve readability
data_paths = ["data/", "2024/data/", "../data/"]

def load_data(input_file):
    file_name = None
    possible_files = [path + input_file for path in data_paths]
    # find the right data path when called from the root directory or from the src directory
    for file_name in possible_files:
        if os.path.exists(file_name):
            break
    else:
        raise FileNotFoundError(f"Input file not found: {input_file}")

    with open(file_name, "r") as f:
        lines = f.read().splitlines()

    equations = [Equations(line) for line in lines]

    return equations


class Equations:
    def __init__(self, equation):
        
        parts = equation.split(": ")
        self.result = int(parts[0])
        self.operands = [int(op) for op in parts[1].split()]

    def __str__(self):
        return f"{self.result} = {' _ '.join(str(op) for op in self.operands)}"
    
    def __repr__(self):
        return f"{self.result} = {' _ '.join(str(op) for op in self.operands)}"
    
    def _brute_force(self, arr, target, index, current_result, operators=["+", "*"]):
        if index == len(arr):
            return current_result == target
        for op in operators:
            if op == "+":
                if self._brute_force(arr, target, index + 1, current_result + arr[index]):
                    return True
            elif op == "*":
                if self._brute_force(arr, target, index + 1, current_result * arr[index]):
                    return True
            elif op == "|":
                if self._brute_force(arr, target, index + 1, int(str(current_result) + str(arr[index]))):
                    return True
        return False
    
    def calibration(self, operators=["+", "*"]):
        return self._brute_force(self.operands, self.result, 1, self.operands[0], operators=operators)
        
### Unit tests ###

class TestAdventOfCodeDay(unittest.TestCase):
    def setUp(self):
        """
        Set up test data for unit tests.
        """

    def test_load_data(self):
        equations = load_data("test_07.txt")
        for eq in equations:
            print(eq)
        print()

    def test_calibration(self):
        equations = load_data("test_07.txt")
        total = sum([ eq.result for eq in equations if eq.calibration(operators=["+", "*"])])
        self.assertEqual(total, 3749)

    def test_adjusted_calibration(self):
        equations = load_data("test_07.txt")
        self.assertTrue( equations[4].calibration(operators=["+", "*", "|"]) )

        for eq in equations:
            print(eq, eq.calibration(operators=["+", "*", "|"]))

        total = sum([ eq.result for eq in equations if eq.calibration(operators=["+", "*", "|"])])
        self.assertEqual(total, 11387)
        print(total)
        

# main function

def main():
    input_file = "07.txt"
    equations = load_data(input_file)
    total = sum([ eq.result for eq in equations if eq.calibration()])
    print("Total:", total)



if __name__ == "__main__":
    import sys 

    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # Run tests
        unittest.main(argv=[sys.argv[0]])
    else:
        # Execute the main function
        main()
