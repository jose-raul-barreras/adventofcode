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
        lines = f.read().splitlines()
    data = [list(line) for line in lines]
    return data

def get_strings_horizontal(data):
    """
    Get all the strings in the matrix by reading the rows.
    """
    strings = []
    for i in range(len(data)):
        strings.append(''.join(data[i]))
    return strings

def get_strings_vertical(data):
    """
    Get all the strings in the matrix by reading the columns.
    """
    strings = []
    for i in range(len(data)):
        strings.append(''.join([data[j][i] for j in range(len(data))]))
    return strings

def get_strings_diagonal_top_left_bottom_right(data):
    """
    Get all the strings in the matrix by reading the diagonals from top-left to bottom-right.
    """
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
    """
    Get all the strings in the matrix by reading the diagonals from top-right to bottom-left.
    """
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

def find_locations(data, search_string):
    locations = []
    n = len(data)
    search_len = len(search_string)
    
    # Check diagonals from top-left to bottom-right
    for i in range(n):
        for j in range(n):
            if i + search_len <= n and j + search_len <= n:
                # Check forward diagonal
                if ''.join(data[i + k][j + k] for k in range(search_len)) == search_string:
                    locations.append((i, j))
                # Check backward diagonal
                if ''.join(data[i + k][j + k] for k in range(search_len)) == search_string[::-1]:
                    locations.append((i, j))
    
    # Check diagonals from top-right to bottom-left
    for i in range(n):
        for j in range(n):
            if i + search_len <= n and j - search_len >= -1:
                # Check forward diagonal
                if ''.join(data[i + k][j - k] for k in range(search_len)) == search_string:
                    locations.append((i, j))
                # Check backward diagonal
                if ''.join(data[i + k][j - k] for k in range(search_len)) == search_string[::-1]:
                    locations.append((i, j))
    
    return locations

def count_x_shaped_string(grid):
    if not grid or not grid[0]:
        return 0
    
    rows, cols = len(grid), len(grid[0])
    count = 0
    
    def check_x_pattern(r, c):
        patterns = 0
        # Check if we can form an X (need 1 space in each direction)
        if r < 1 or r >= rows-1 or c < 1 or c >= cols-1:
            return 0
            
        # Possible MAS/SAM combinations for each diagonal
        valid_patterns = ["MAS", "SAM"]
        
        # Check all combinations of diagonals
        for p1 in valid_patterns:
            for p2 in valid_patterns:
                # Top-left to bottom-right + Top-right to bottom-left
                if (grid[r-1][c-1] == p1[0] and grid[r][c] == p1[1] and grid[r+1][c+1] == p1[2] and
                    grid[r-1][c+1] == p2[0] and grid[r][c] == p2[1] and grid[r+1][c-1] == p2[2]):
                    patterns += 1

        return patterns

    # Check each possible center position
    for i in range(rows):
        for j in range(cols):
            count += check_x_pattern(i, j)
            
    return count

class TestAdventOfCodeDay(unittest.TestCase):
    def setUp(self):
        """
        Set up test data for unit tests.
        """

        self.test_data = [[
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
        ],
        ]
        self.answers = [9]

    def test_count_string(self):
        """
        Test count_string function.
        """
        self.assertEqual(count_string(self.test_data[0], "XMAS"), 18)
 
    def test_load_data(self):
        """
        Test load_data function.
        """
        data = load_data('04.txt')
        print("Number of lines: ", len(data))
        print("Number of characters in each line: ", len(data[0]))
        self.assertIsNotNone(data)

    def test_count_x_shaped_string(self):
        """
        Test count_x_shaped_string function.
        """
        for i in range(len(self.test_data)):
            self.assertEqual(count_x_shaped_string(self.test_data[i]), self.answers[i])


def main():
    input_file = '04.txt'
    data = load_data(input_file)
    search_string = "XMAS"
    print(f"Number of occurences of '{search_string}': ", count_string(data, search_string))
    print(f"Number of occurences of X-shaped 'MAS': ", count_x_shaped_string(data))

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # Run tests
        unittest.main(argv=[sys.argv[0]])
    else:
        # Execute the main function
        main()