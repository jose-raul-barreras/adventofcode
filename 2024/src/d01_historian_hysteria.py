# https://adventofcode.com/2024/day/1


def total_distance(left_list, right_list):
    res = 0
    # unique values
    left_sorted = sorted(left_list)
    right_sorted = sorted(right_list)

    # min length
    min_len = min(len(left_sorted), len(right_sorted))

    # total distance
    for i in range(min_len):
        res += abs(left_sorted[i] - right_sorted[i])

    return res

def similarity_score(left_list, right_list):
    res = 0
    for left_element in left_list:
        count = 0
        for right_element in right_list:
            if left_element == right_element:
                count += 1
        res += left_element * count
    return res

# Test cases
print("Testing test data...")


left_list  = [3, 4, 2, 1, 3, 3]
right_list = [4, 3, 5, 3, 9, 3]
test_total_distance = 11
test_similarity_score = 31

def test_total_distance():
    assert test_total_distance == total_distance(left_list, right_list)

def test_similarity_score():
    assert 31 == similarity_score(left_list, right_list)


file_name = '../data/01.txt'
left_list = []
right_list = []
i = 0
with open(file_name, 'r') as f:
    input = f.read().split("\n")
f.close()

for data in input:
    left_list.append(int(data.split()[0]))
    right_list.append(int(data.split()[1]))

print("Result: ", total_distance(left_list, right_list))
print("Result: ", similarity_score(left_list, right_list))
