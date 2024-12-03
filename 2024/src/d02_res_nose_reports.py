#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import os

# https://adventofcode.com/2024/day/2

def is_safe_report(report):
    safe = True
    if report == sorted(report) or report == sorted(report, reverse=True):
        for i in range(len(report) - 1):
            diff = report[i] - report[i + 1]
            if abs(diff) > 3 or diff == 0:
                safe = False
                break
    else:
        safe = False
    return safe

def safe_reports(reports):
    res = 0
    for report in reports:
        if is_safe_report(report):
            res += 1
    return res

def safe_reports_with_problem_dampener(reports):
    res = 0
    for report in reports:
        for i in range(len(report)):
            # delete element i
            if is_safe_report(report[:i] + report[i + 1:]):
                res += 1
                break
    return res

class TestAdventOfCodeDay2(unittest.TestCase):
    def setUp(self):
        """
        Set up test data for unit tests.
        """
        self.reports = [
            [7, 6, 4, 2, 1],
            [1, 2, 7, 8, 9],
            [9, 7, 6, 2, 1],
            [1, 3, 2, 4, 5],
            [8, 6, 4, 4, 1],
            [1, 3, 6, 7, 9]
        ]

    def test_safe_report(self):
        """
        Test safe_report function.
        """
        self.assertEqual(safe_reports(self.reports), 2)

    def test_safe_reports_with_problem_dampener(self):
        """
        Test safe_reports_with_problem_dampener function.
        """
        self.assertEqual(safe_reports_with_problem_dampener(self.reports), 4)

def load_data(input_file):
    # find the rigth data path when called from the root directory or from the src directory
    paths = ['data/' + input_file, '2024/data/' + input_file, '../data/' + input_file]
    for file_name in paths:
        if os.path.exists(file_name):
            break
    if not os.path.exists(file_name):
        raise FileNotFoundError(f"Input file not found: {input_file}")

    reports = []
    with open(file_name, 'r') as f: input = f.read().split("\n")
    reports = [list(map(int, x.split())) for x in input]
    return reports

def main():
    input_file = '02.txt'
    reports = load_data(input_file)

    print("Safe reports: ", safe_reports(reports))
    print("Safe reports with problem dampener: ", safe_reports_with_problem_dampener(reports))

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # Run tests
        unittest.main(argv=[sys.argv[0]])
    else:
        # Execute the main function
        main()