# https://adventofcode.com/2023/day/4

import re

class Card():
    id = None
    numbers = []
    winning_numbers = []
    copies = None

    def __init__(self, line, copies = 1) -> None:
        self.id = int(re.sub(' +', ' ', line.split(":")[0]).strip().split()[1])
        self.winning_numbers = [int(number.strip()) for number in line.split(":")[1].split('|')[0].strip().split(" ") if number != ""]
        self.numbers = [int(number.strip()) for number in line.split(":")[1].split('|')[1].strip().split(" ") if number != ""]
        self.copies = copies
        
    def value(self):
        return len([1 for number in self.numbers if number in self.winning_numbers])

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
        for pos in range(len(self.cards)):
            _cur_card_copies = self.cards[pos].copies #qa
            for reps in range(self.cards[pos].copies):
                _cur_card_value = self.cards[pos].value() # qa
                _affected_ids = [ c.id for c in self.cards[pos+1:pos+1+self.cards[pos].value()] ] #qa
                if self.cards[pos].value() > 0:
                    for card in self.cards[pos+1:pos+1+self.cards[pos].value()]:
                        card.copies += 1

    def total_worth(self):
        values = [card.value() for card in self.cards]
        print(values)
        return sum(values)
    
    def total_cards(self):
        return sum([card.copies for card in self.cards])
    
    def __str__(self):
        return "\n".join([f"{str(card.copies)} - {card.__str__()}" for card in self.cards])

file_name = "2023/data/04_test_cases.txt"
test_pile = ScratchcardsPile(file_name)
print(test_pile)
assert test_pile.total_cards() == 30

file_name = "2023/data/04_input.txt"
pile = ScratchcardsPile(file_name)
print(pile.total_cards())
