from os import getcwd
DATA_DIR = getcwd() + "/2021/data/"

def load_level_input(level):
    try:
        file_name = DATA_DIR + str(level)
        with open(file_name, 'r') as f:
            input = f.read().split("\n")
        input = [int(i) for i in input]
    except FileNotFoundError:
        input = []
    return input
