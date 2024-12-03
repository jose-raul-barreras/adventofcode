# https://adventofcode.com/2023/day/1#part2

NUMBERS = {'one':'o1e', 'two':'t2o', 'three':'t3e', 'four':'f4r', 'five':'f5e', 'six':'s6x', 'seven':'s7n', 'eight':'e8t', 'nine':'n9e'}

def words_to_numbers(input, debug=False):
    pos = [(input.find(key), key) for key in NUMBERS.keys() if key in input]
    sorted_pos = sorted(pos, key=lambda x: x[0])
    cur_pos = 0
    res = ""
    for found_str in sorted_pos:
        if cur_pos < found_str[0]:
            res = res + input[cur_pos:found_str[0]]
            cur_pos = found_str[0]
        if cur_pos == found_str[0]:
            res = res + NUMBERS[found_str[1]]
            last_word_pos = found_str[0] + len(found_str[1]) - 1
        if cur_pos > found_str[0]:
            if last_word_pos == found_str[0]:
                res = res + NUMBERS[found_str[1]]
                last_word_pos = found_str[0] + len(found_str[1]) - 1
            else:
                pass
        cur_pos = found_str[0] + len(found_str[1])
    if cur_pos < len(input):
        res = res + input[cur_pos:]
    return res

def words_to_numbers2(input, debug=False):
    for key in NUMBERS.keys():
        if key in input:
            input = input.replace(key, NUMBERS[key])
    return input

def calc_calibration(input, debug=False):
    tmp = []
    org_input = input.lower()
    input = wtn = words_to_numbers(input, debug)
    for ch in input:
        # ord('0') = 48, ord('9') = 57
        if ord(ch) >= 48 and ord(ch) <= 57:
            tmp.append(ch)
    try:
        res = "".join([tmp[0], tmp[-1]])
    except IndexError:
        return 0
    if debug: print(org_input, " ", wtn, " ", res)
    return int(res)

# Pass test cases
test_data = ['two1nine','eightwothree','abcone2threexyz','xtwone3four','4nineeightseven2','zoneight234','7pqrstsixteen','ninef', '6abc', 'two']
test_res = [29, 83, 13, 24, 42, 14, 76, 99, 66, 22]
print('Testing test data')
assert sum(test_res) == sum([calc_calibration(i, debug=True) for i in test_data]) 

# wtn_2_test_data = ['two1nine','eightwothree','abcone2threexyz','xtwone3four','4nineeightseven2','zoneight234','7pqrstsixteen','ninef', '6abc', 'two', 'one7sixninesix']
# for i in wtn_2_test_data:
#     print(i, " ", words_to_numbers(i))


print('Calculating calibration')
file_name = '2023/data/01.txt'
# file_name = '2023/data/01_test_cases.txt'
with open(file_name, 'r') as f:
    input = f.read().split("\n")

print(sum([calc_calibration(i, debug=True) for i in input]))
