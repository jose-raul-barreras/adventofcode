#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import unittest
import math 

# https://adventofcode.com/2024/day/8

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

    # return a list of dictionaries where the data is the list of positions and the value is the character
    grid = {}
    grid_size = (len(lines[0]), len(lines))
    for y, line in enumerate(lines):
        for x, ch in enumerate(line):
            
            if ch in grid.keys():
                grid[ch].append((x, y))
            else:
                grid[ch] = [(x, y)]

    return grid, grid_size

def print_grid(grid, grid_size):
    for y in range(grid_size[1]):
        for x in range(grid_size[0]):
            for key in grid.keys():
                if (x, y) in grid[key]:
                    print(key, end="")
                    break
            else:
                print(".", end="")
        print()
    print()

def antinodes(x, y):
    p1 = min(x, y)
    p2 = max(x, y)

    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]

    if dy/dx > 0:
        p3 = (p1[0] - dx, p1[1] - dy)
        p4 = (p2[0] + dx, p2[1] + dy)
    elif dy/dx < 0:
        p3 = (p1[0] - dx, p1[1] - dy)
        p4 = (p2[0] + dx, p2[1] + dy)
    else:
        raise ValueError("Invalid slope")
        
    return p3, p4

def get_all_antinodes(grid, grid_size):
    antinodes_list = []
    for key in grid.keys():
        if key in [".", "#"]:
            continue
        if len(grid[key]) > 1:
            # print(key, ":", grid[key])
            for i in range(len(grid[key])-1):
              for j in range(i+1, len(grid[key])):
                for antinode in antinodes(grid[key][i], grid[key][j]):
                    antinodes_list.append(antinode)

    return sorted({ antinode for antinode in antinodes_list if 0 <= antinode[0] < grid_size[0] and 0 <= antinode[1] < grid_size[1]})


### Unit tests ###

class TestAdventOfCodeDay(unittest.TestCase):
    def setUp(self):
        """
        Set up test data for unit tests.
        """

    def test_load_data(self):
        grid, grid_size = load_data("test_08.txt")
        # print(grid.keys())
        antinodes_list = get_all_antinodes(grid, grid_size)
        self.assertEqual(len(antinodes_list), 14)
        # print_grid(grid, grid_size)
        # grid['#'] = antinodes_list
        # print_grid(grid, grid_size)

# main function


def main():
    input_file = "08.txt"
    grid, grid_size = load_data("08.txt")
    # print(grid.keys())
    antinodes_list = get_all_antinodes(grid, grid_size)
    print(len(antinodes_list))
    

if __name__ == "__main__":
    import sys 

    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # Run tests
        unittest.main(argv=[sys.argv[0]])
    else:
        # Execute the main function
        main()
