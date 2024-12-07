#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import unittest
import copy
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
from functools import partial
import multiprocessing as mp

# https://adventofcode.com/2024/day/6

# Constants
UP = "^"
DOWN = "V"
LEFT = "<"
RIGHT = ">"
OBSTACLE = "#"
VISITED = "X"
OUT_OF_BOUNDS = "O"
GUARD_ORIENTATIONS = [UP, DOWN, LEFT, RIGHT]

# a guard is a tuple of a position and an orientation
guard = ((0, 0), UP)

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

    # floor map is a list of strings representing the floor map
    floor_map = []
    with open(file_name, "r") as f:
        lines = f.read().splitlines()

    floor_map.append(list(OUT_OF_BOUNDS * (len(lines[0]) + 2)))
    for line in lines:
        floor_map.append(list(OUT_OF_BOUNDS + line + OUT_OF_BOUNDS))
    floor_map.append(list(OUT_OF_BOUNDS * (len(lines[0]) + 2)))

    return floor_map


def print_floor_map(floor_map):
    # wait 0.1 seconds and clear the screen
    # time.sleep(0.1)
    #print("\033[2J")
    print()
    # print the floor map
    for row in floor_map:
        for col in row:
            if col == OBSTACLE:
                print("#", end="")
            elif col in GUARD_ORIENTATIONS:
                # print the guard as a caret in dark red
                print("\033[91m" + col, end="")
            else:
                # print the floor as a white dot
                print("\033[97m.", end="")
        print("")

def get_guard(floor_map):
    for row in range(1, len(floor_map)-1):
        for col in range(1, len(floor_map[0])-1):
            if floor_map[row][col] in GUARD_ORIENTATIONS:
                return ((row, col), floor_map[row][col])
    return None
      
def set_guard(floor_map, guard):
    ((row, col), orientation) = guard
    floor_map[row][col] = orientation
    return floor_map

def out_of_bounds(floor_map, position):
    return position[0] < 1 or position[0] >= len(floor_map)-1 or position[1] < 1 or position[1] >= len(floor_map[0])-1

def move_guard(floor_map, guard):
    (position, orientation) = guard
    if orientation == UP:
        if floor_map[position[0]-1][position[1]] == OBSTACLE:
            orientation = RIGHT
        else:
            position = (position[0]-1, position[1])
            floor_map[position[0]][position[1]] = orientation
    elif orientation == DOWN:
        if floor_map[position[0]+1][position[1]] == OBSTACLE:
            orientation = LEFT
        else:
            position = (position[0]+1, position[1])
            floor_map[position[0]][position[1]] = orientation
    elif orientation == LEFT:
        if floor_map[position[0]][position[1]-1] == OBSTACLE:
            orientation = UP
        else:
            position = (position[0], position[1]-1)
            floor_map[position[0]][position[1]] = orientation
    elif orientation == RIGHT:
        if floor_map[position[0]][position[1]+1] == OBSTACLE:
            orientation = DOWN
        else:
            position = (position[0], position[1]+1)
            floor_map[position[0]][position[1]] = orientation
    return (position, orientation)


def count_visited(floor_map):
    count = 0
    for row in floor_map:
        for col in row:
            if col in GUARD_ORIENTATIONS:
                count += 1
    return count-1 # do not count the initial position

def run_shift(floor_map, guard):
    (position, orientation) = guard
    path = []
    while not out_of_bounds(floor_map, position):
        # insert the current position into the path if the last position is not the same
        if len(path) == 0 or path[-1] != position:
            path.append(position)
        guard = move_guard(floor_map, guard)
        (position, orientation) = guard
        
    return path

# second part

def is_a_loop(floor_map, guard):
    (position, orientation) = guard
    path = []
    while not out_of_bounds(floor_map, position) and (guard not in path):
        path.append(guard)
        guard = move_guard(floor_map, guard)
        (position, orientation) = guard

    return not out_of_bounds(floor_map, position)

def progress_bar_and_traps(current, total, traps, bar_length=60):
    progress = current / total
    arrow = "=" * int(progress * bar_length - 1) + ">"
    spaces = " " * (bar_length - len(arrow))
    print(f"Progress: [{arrow + spaces}] {current}/{total} -- {traps}", end="\r")

def count_traps(floor_map, guard):
    traps = []
    total_positions = (len(floor_map) - 2) * (len(floor_map[0]) - 2)
    
    def check_position(row, col):
        test_floor_map = copy.deepcopy(floor_map)
        test_floor_map[row][col] = "#"
        if is_a_loop(test_floor_map, guard):
            return (row, col)
        return None

    with ThreadPoolExecutor() as executor:
        futures = []
        for row in range(1, len(floor_map) - 1):
            for col in range(1, len(floor_map[0]) - 1):
                futures.append(executor.submit(check_position, row, col))
        
        for i, future in enumerate(futures):
            result = future.result()
            if result:
                traps.append(result)
            progress_bar_and_traps(i + 1, total_positions, len(traps))
    
    return traps

# Move check_position outside to make it pickleable
def check_position(args):
    row, col, floor_map, guard = args
    test_floor_map = copy.deepcopy(floor_map)
    test_floor_map[row][col] = "#"
    if is_a_loop(test_floor_map, guard):
        return (row, col)
    return None

def count_traps_with_pool_executor(floor_map, guard):
    traps = []
    total_positions = (len(floor_map) - 2) * (len(floor_map[0]) - 2)
    
    # Create arguments list
    positions = [
        (row, col, floor_map, guard)
        for row in range(1, len(floor_map) - 1)
        for col in range(1, len(floor_map[0]) - 1)
    ]
    
    # Use max_workers based on CPU cores
    max_workers = mp.cpu_count()
    
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        for i, result in enumerate(executor.map(check_position, positions)):
            if result:
                traps.append(result)
            progress_bar_and_traps(i + 1, total_positions, len(traps))
    
    return traps

class TestAdventOfCodeDay(unittest.TestCase):
    def setUp(self):
        """
        Set up test data for unit tests.
        """

    def test_load_data(self):
        floor_map = load_data("test_06.txt")
        self.assertEqual(len(floor_map), 12)
        self.assertEqual(len(floor_map[0]), 12)
        guard = get_guard(floor_map)
        # print_floor_map(floor_map)
        # print(guard)
        path = run_shift(floor_map, guard)
        self.assertEqual(count_visited(floor_map), 41)

    def test_is_a_loop(self):
        floor_map = load_data("test_06.txt")
        guard = get_guard(floor_map)
        self.assertEqual(is_a_loop(floor_map, guard), False)
        floor_map_1 = floor_map
        floor_map_1[7][4] = "#"
        self.assertEqual(is_a_loop(floor_map, guard), True)
        floor_map_2 = floor_map
        floor_map_2[8][7] = "#"
        self.assertEqual(is_a_loop(floor_map, guard), True)
        floor_map_3 = floor_map
        floor_map_3[9][4] = "#"
        self.assertEqual(is_a_loop(floor_map, guard), True)
        floor_map_4 = floor_map
        floor_map_4[8][10] = "#"
        self.assertEqual(is_a_loop(floor_map, guard), True)

    def test_count_traps(self):
        floor_map = load_data("test_06.txt")
        guard = get_guard(floor_map)   
        self.assertEqual(len(count_traps_with_pool_executor(floor_map, guard)), 6)

def main():
    input_file = "05.txt"
    floor_map = load_data("06.txt")
    guard = get_guard(floor_map)   
    path = run_shift(floor_map, guard)
    print ("Number of steps:", count_visited(floor_map))

    traps = count_traps_with_pool_executor(floor_map, guard)
    print("Number of traps:", len(traps))


if __name__ == "__main__":
    import sys 

    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # Run tests
        unittest.main(argv=[sys.argv[0]])
    else:
        # Execute the main function
        main()


# # Different approach, heuristic, not tested yet

# def find_horinzontal_lines(floor_map):
#     lines = []
#     for row in range(1, len(floor_map)-1):
#         line = []
#         for col in range(1, len(floor_map[0])-1):
#             if floor_map[row][col] == OBSTACLE:
#                 if line:
#                     lines.append(line)
#                     line = []
#             else:
#                 line.append((row, col))
#         if line:
#             lines.append(line)
#     return [line for line in lines if len(line) > 1]

# def find_vertical_lines(floor_map):
#     lines = []
#     for col in range(1, len(floor_map[0])-1):
#         line = []
#         for row in range(1, len(floor_map)-1):
#             if floor_map[row][col] == OBSTACLE:
#                 if line:
#                     lines.append(line)
#                     line = []
#             else:
#                 line.append((row, col))
#         if line:
#             lines.append(line)
#     return [line for line in lines if len(line) > 1]

# def overlap_horizontal_lines(line1, line2):
#     set1 = set(line1).intersection([(line1[0][0], point[1]) for point in line2])
#     set2 = set(line2).intersection([(line2[0][0], point[1]) for point in line1])
#     return [sorted(set1), sorted(set2)]

# def overlap_vertical_lines(line1, line2):
#     set1 = set(line1).intersection([(point[0],line1[0][1]) for point in line2])
#     set2 = set(line2).intersection([(point[0],line2[0][1]) for point in line1])
#     return [sorted(set1), sorted(set2)]

# def get_surronding_points(floor_map, point):
#     row, col = point
#     possible_points = [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]
#     return [point for point in possible_points if floor_map[point[0]][point[1]] not in [OBSTACLE, OUT_OF_BOUNDS]]