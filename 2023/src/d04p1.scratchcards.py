# https://adventofcode.com/2023/day/4

class Card():
    id = None
    numbers = []
    winning_numbers = []

    def __init__(self, line) -> None:
        self.id = line.split(":")[0].split(" ")[1].strip()
        self.winning_numbers = [int(number.strip()) for number in line.split(":")[1].split('|')[0].strip().split(" ") if number != ""]
        self.numbers = [int(number.strip()) for number in line.split(":")[1].split('|')[1].strip().split(" ") if number != ""]
        pass

    def value(self):
        res = 0
        winners = [1 for number in self.numbers if number in self.winning_numbers]
        if len(winners) > 0:
            res = 2**(len(winners)-1)
        return res


    def __str__(self):
        winning_numbers = " ".join([str(number) for number in self.winning_numbers])
        numbers = " ".join([str(number) for number in self.numbers])
        return f"Card {self.id}: {winning_numbers}|{numbers}"


class ScratchcardsPile():
    cards = []

    def __init__(self, file_name) -> None:
        self.load_data(file_name)

    def load_data(self, file_name):
        with open(file_name, 'r') as f:
            input = f.read().split("\n")
        self.cards = [Card(card) for card in input if card != ""]

    def total_worth(self):
        values = [card.value() for card in self.cards]
        print(values)
        return sum(values)
        
    def __str__(self):
        return "\n".join([card.__str__() for card in self.cards])

file_name = "2023/data/04_test_cases.txt"
test_pile = ScratchcardsPile(file_name)
print(test_pile)
assert test_pile.total_worth() == 13

file_name = "2023/data/04_input.txt"
pile = ScratchcardsPile(file_name)
print(pile.total_worth())
