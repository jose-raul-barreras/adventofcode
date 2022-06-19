def solve(input):
    increments = 0
    for i in range(1,len(input)):
        if input[i] > input[i-1]:
            increments += 1
    return increments

def test_solution():
    input = [199,200,208,210,200,207,240,269,260,263]
    assert solve(input) == 7
