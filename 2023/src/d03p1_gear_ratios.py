#https://adventofcode.com/2023/day/3

SYMBOLS=set(['*','#','$','+','/','-', '%', '&', '@', '='])
DIGITS=set(['0','1','2','3','4','5','6','7','8','9'])
DOT=set(['.'])
        
class Schematic():
    m = []
    numbers = []
    valid_numbers = []
    invalid_numbers = []
    def __init__(self, file_name) -> None:
        self.load_data(file_name)
        is_valid_schematic, bad_elements = self.valid_schematic()
        if not is_valid_schematic:
            raise ValueError("Bad elements in schematic: {}".format(bad_elements))
        self.find_numbers()
        self.calculate_valid_numbers()

    def load_data(self, file_name):
        with open(file_name, 'r') as f:
            input = f.read().split("\n")
        self.m = ['.'+line+'.' for line in input if line != ""]
        self.m.append('.'*len(self.m[0]))
        self.m.insert(0, '.'*len(self.m[0]))

    def __str__(self):
        return "\n".join([line for line in self.m])

    def valid_schematic(self):
        res = True
        bad_elements = []
        for line in self.m:
            for element in line:
                if element not in DIGITS.union(SYMBOLS).union(DOT):
                    bad_elements.append(element)
                    res = False
        return res, set(bad_elements)
    
    def find_numbers(self):
        numbers = []
        x = 0
        for line in self.m:
            j = 0
            while j < len(line):
                if line[j] in DIGITS:
                    a_j = line[j]
                    y1 = y2 = j
                    while line[y2] in DIGITS and y2 < len(line):
                        y2 += 1
                    sub = line[y1:y2]
                    numbers.append([(x,y1,y1+len(sub)), sub])
                    j = y2-1
                j += 1
            x += 1
        self.numbers = numbers

    def calculate_valid_numbers(self):
        for number in self.numbers:
            r = number[0][0]
            c1 = number[0][1]
            c2 = number[0][2]
            l1 = self.m[r-1][c1-1:c2+1]
            l2 = self.m[r][c1-1] +self.m[r][c2]
            l3 = self.m[r+1][c1-1:c2+1]
            found = [True for symbol in SYMBOLS if symbol in l1 or symbol in l2 or symbol in l3]
            if any(found):
                self.valid_numbers.append(int(number[1]))

            
# file_name = '2023/data/03_test_cases.txt'
# sch = Schematic(file_name=file_name)
# print(sch)
# print(sch.valid_numbers)
# # assert sum(sch.valid_numbers) == 4361
# sch = None

file_name = '2023/data/03_input.txt'
sch = Schematic(file_name=file_name)
#print(sch.valid_numbers)
print(sum(sch.valid_numbers))
# print(len(sch.invalid_numbers))
# print(sum(sch.valid_numbers))
