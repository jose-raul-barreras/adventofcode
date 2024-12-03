# https://adventofcode.com/2023/day/2


class Round():
    red = 0
    blue = 0
    green = 0
    def __init__(self, input="0 red, 0 blue, 0 green"):
        try:
            colors = input.split(",")
            for color in colors:
                count = int(color.strip().split(" ")[0])
                if 'red' in color.strip().split(" ")[1].lower():
                    self.red = count
                elif 'blue' in color.strip().split(" ")[1].lower():
                    self.blue = count 
                elif 'green' in color.strip().split(" ")[1].lower():
                    self.green = count
                else:
                    pass
        except IndexError:
            pass

    def power(self):
        return self.red * self.green * self.blue

    def as_rgb(self):
        return [self.red, self.green, self.blue]
    
    def __str__(self):
        return f"{self.red} {self.green} {self.blue} "

class Game():
    id = int
    rounds = []
    def __init__(self, input):
        try:
            self.id = int(input.split(":")[0].split(" ")[1])
            self.rounds = [Round(round) for round in input.split(":")[1].split(";")]
        except IndexError:
            self.id = None

    def is_valid(self, max_round=Round("0 red, 0 blue, 0 green")):
        if self.id is None:
            return False
        else:
            return all([True if (round.red <= max_round.red) and (round.blue <= max_round.blue) and (round.green <= max_round.green) else False for round in self.rounds ])
    
    def minimum_set_of_cubes(self):
        minimum = Round()
        minimum.red = max([round.red for round in self.rounds])
        minimum.blue = max([round.blue for round in self.rounds])
        minimum.green = max([round.green for round in self.rounds])
        return minimum

    def __str__(self):
        res = f"{self.id}:" + "".join([round.__str__() + ";" for round in self.rounds])
        return res

class GameSession():
    games = []
    def __init__(self, file_name):
        self.load_data(file_name)

    def valid_games(self, max_round=Round("0 red, 0 blue, 0 green")):
        return [game.id for game in self.games if game.is_valid(max_round=max_round)]

    def __str__(self):
        return "".join([game.__str__() + "\n" for game in self.games])

    def minimums(self):
        return [game.minimum_set_of_cubes() for game in self.games]

    def load_data(self, file_name):
        with open(file_name, 'r') as f:
            input = f.read().split("\n")
        self.games = [Game(line) for line in input if line != ""]

## tests 
max_round = Round('12 red, 13 green, 14 blue')
game_session = GameSession('2023/data/02p1_test_cases.txt')
assert sum(game_session.valid_games(max_round=max_round)) == 8
minimums = [cube_set.as_rgb() for cube_set in game_session.minimums()]
assert minimums == [
    [4,2,6],
    [1,3,4],
    [20,13,6], 
    [14,3,15],
    [6,3,2]] 

cubes = [cube_set.power() for cube_set in game_session.minimums()] 
assert cubes == [48, 12, 1560, 630, 36]
assert sum(cubes) == 2286
        
## solve problem 
game_session = GameSession('2023/data/02_input.txt')
cubes = [cube_set.power() for cube_set in game_session.minimums()] 
print(sum(cubes))
