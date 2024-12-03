# https://adventofcode.com/2023/day/1

def calc_calibration(input, debug=False):
    tmp = []
    input = input.lower()
    for ch in input:
        # ord('0') = 48, ord('9') = 57
        if ord(ch) >= 48 and ord(ch) <= 57:
            tmp.append(ch)
    try:
        res = "".join([tmp[0], tmp[-1]])
    except IndexError:
        return 0
    if debug: print(input, " ", res)
    return int(res)

# Pass test cases
test_data = ['1abc2', 'pqr3stu8vwx', 'a1b2c3d4e5f', 'treb7uchet']
test_res = [12, 38, 15, 77]
print("Testing test data")
assert sum(test_res) == sum([calc_calibration(i, debug=True) for i in test_data]) == 142


file_name = 'data/01.txt'
with open(file_name, 'r') as f:
    input = f.read().split("\n")

print(sum([calc_calibration(i) for i in input]))
