#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import unittest
import time

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
        print_floor_map(floor_map)
        print(guard)
        path = run_shift(floor_map, guard)
        self.assertEqual(count_visited(floor_map), 41)
        print_floor_map(floor_map)
        print(path)

        print("Number of steps:", count_visited(floor_map))

    # def test_find_guard(self):
    #     floor_map = load_data("test_06.txt")
    #     guard_shift = GuardShift(floor_map)
    #     self.assertEqual(guard_shift.position, (7, 5))
    #     self.assertEqual(guard_shift.guard, "^")

    # # def test_run_shift(self):
    # #     floor_map = load_data("test_06.txt")
    # #     guard_shift = GuardShift(floor_map)
    # #     guard_shift.run_shift()

    # def test_count_visited(self):
    #     floor_map = load_data("test_06.txt")
    #     guard_shift = GuardShift(floor_map)
    #     guard_shift.run_shift()
    #     self.assertEqual(guard_shift.count_visited(), 40)
    #     guard_shift.print_floor_map()
    #     print(len(guard_shift.path))

    # def test_possible_traps(self):
    #     floor_map = load_data("test_06.txt")
    #     guard_shift = GuardShift(floor_map)
    #     print("Possible traps:")
    #     for trap in guard_shift.find_traps():
    #         print(trap)

    # def test_find_horizontal_lines(self):
    #     floor_map = load_data("test_06.txt")
    #     guard_shift = GuardShift(floor_map)
    #     print("Horizontal lines:")
    #     for line in guard_shift.find_horinzontal_lines():
    #         print(line)
    
    # def test_find_vertical_lines(self):
    #     floor_map = load_data("test_06.txt")
    #     guard_shift = GuardShift(floor_map)
    #     print("Vertical lines:")
    #     for line in guard_shift.find_vertical_lines():
    #         print(line)

    # def test_count_traps(self):
    #     floor_map = load_data("test_06.txt")
    #     guard_shift = GuardShift(floor_map)
    #     bk_map = floor_map
    #     tmp_floor_map = floor_map
    #     tmp_floor_map[7][4] = "#"
    #     guard_shift.print_floor_map(tmp_floor_map)
    #     print("is a loop:", guard_shift.is_a_loop(tmp_floor_map, guard_shift.guard, guard_shift.position))
    #     guard_shift.floor_map = bk_map
    #     print("Count traps:", guard_shift.count_traps(tmp_floor_map))

def main():
    input_file = "05.txt"
    floor_map = load_data("06.txt")
    guard = get_guard(floor_map)   
    path = run_shift(floor_map, guard)
    print ("Number of steps:", count_visited(floor_map))


if __name__ == "__main__":
    import sys 

    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # Run tests
        unittest.main(argv=[sys.argv[0]])
    else:
        # Execute the main function
        main()
