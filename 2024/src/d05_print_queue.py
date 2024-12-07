#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from unittest.mock import patch
import os

# https://adventofcode.com/2024/day/5


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

    # ordering_rules is a list of page numbers (a,b) where the element a should appear before element b
    # pages_to_print is a list of page numbers to print (x,...,z) 
    ordering_rules = []
    pages_to_print = []
    with open(file_name, "r") as f:
        lines = f.read().splitlines()
    for line in lines:
        if "|" in line:
            ordering_rules.append((int(line.split('|')[0]), int(line.split('|')[1])))
        if "," in line:
            pages_to_print.append([int(x) for x in line.split(",")])

    return ordering_rules, pages_to_print

def in_order(ordering_rules, pages_list):
    """
    Check if the pages to print are in the correct order.
    """
    for i in range(len(pages_list) - 1):
        for j in range(i+1, len(pages_list)):
            if (pages_list[j], pages_list[i]) in ordering_rules:
                return False    
    return True

def middle_page_number_sum(ordering_rules, pages_to_print):
    """
    Find the sum of the middle page numbers if the pages are in order.
    """
    sum = 0
    for pages_list in pages_to_print:
        if in_order(ordering_rules, pages_list):
            sum += pages_list[len(pages_list) // 2]          
    return sum

def get_incorrectly_ordered_pages(ordering_rules, pages_to_print):
    """
    Get a list of pages that are not in order.
    """
    incorrect_pages = []
    for pages_list in pages_to_print:
        if not in_order(ordering_rules, pages_list):
            incorrect_pages.append(pages_list)
    return incorrect_pages

def set_pages_in_order(ordering_rules, pages_list):
    """
    Set the pages in the correct order.
    """
    for i in range(len(pages_list) - 1):
        for j in range(i+1, len(pages_list)):
            if (pages_list[j], pages_list[i]) in ordering_rules:
                pages_list[i], pages_list[j] = pages_list[j], pages_list[i]
    return pages_list

class TestAdventOfCodeDay(unittest.TestCase):
    def setUp(self):
        """
        Set up test data for unit tests.
        """

    def test_load_data(self):
        ordering_rules, pages_to_print = load_data("test_05.txt")
        self.assertEqual(len(ordering_rules), 21)
        self.assertEqual(len(pages_to_print), 6)

    def test_middle_page_number_sum(self):
        ordering_rules, pages_to_print = load_data("test_05.txt")
        self.assertEqual(middle_page_number_sum(ordering_rules, pages_to_print), 143)

    def test_incorrectly_ordered_pages(self):
        ordering_rules, pages_to_print = load_data("test_05.txt")
        incorrectly_ordered_pages = get_incorrectly_ordered_pages(ordering_rules, pages_to_print)
        sorted_incorrectly_ordered_pages = []
        for pages_list in incorrectly_ordered_pages:
            sorted_incorrectly_ordered_pages.append(set_pages_in_order(ordering_rules, pages_list))
        self.assertEqual(middle_page_number_sum(ordering_rules, sorted_incorrectly_ordered_pages), 123)

def main():
    input_file = "05.txt"
    data = load_data(input_file)
    ordering_rules, pages_to_print = load_data("05.txt")
    print("Sum of middle page numbers: ", middle_page_number_sum(ordering_rules, pages_to_print))


    incorrectly_ordered_pages = get_incorrectly_ordered_pages(ordering_rules, pages_to_print)
    sorted_incorrectly_ordered_pages = []
    for pages_list in incorrectly_ordered_pages:
        sorted_incorrectly_ordered_pages.append(set_pages_in_order(ordering_rules, pages_list))

    print("Sum of middle page numbers with correctly ordered pages: ", middle_page_number_sum(ordering_rules, sorted_incorrectly_ordered_pages))



if __name__ == "__main__":
    import sys 

    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # Run tests
        unittest.main(argv=[sys.argv[0]])
    else:
        # Execute the main function
        main()
