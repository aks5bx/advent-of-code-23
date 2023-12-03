import time


def read_games():
    with open('day2/puzzle_input.txt', 'r') as f:
        return f.readlines()


def save_outcome(outcome, outcome_dict):
    outcome = outcome.strip().replace(',', '').split(' ')

    for i in range(0, len(outcome), 2):
        amount = int(outcome[i])
        color = outcome[i+1]
        outcome_dict[color].append(amount)
    
    return outcome_dict


def parse_game(game_line):


    outcome_dict = {'red' : [], 
                    'blue' : [],
                    'green' : []}

    # Get Game Number
    game, info = game_line.split(':')
    game_num = int(game.split(" ")[1])

    # Get Game Outcomes
    outcomes = info.split(';')
    for outcome in outcomes:
        outcome_dict = save_outcome(outcome, outcome_dict)

    return game_num, outcome_dict


def validate_outcome(outcome_dict):
    # Red Condition 
    if max(outcome_dict['red']) > 12:
        return False
    elif max(outcome_dict['green']) > 13:
        return False
    elif max(outcome_dict['blue']) > 14:
        return False
    else:
        return True
    

def get_game_power(outcome_dict):
    red = max(outcome_dict['red'])
    green = max(outcome_dict['green'])
    blue = max(outcome_dict['blue'])

    power = red * green * blue
    return power
    

def analyze_games(power=False):
    games = read_games()

    if power == False:
        valid_games = []
        for game in games:
            game_num, outcome_dict = parse_game(game)
            if validate_outcome(outcome_dict):
                valid_games.append(game_num)

        game_sum = sum(valid_games)
        return game_sum
    else:
        power_sum = 0
        for game in games:
            game_num, outcome_dict = parse_game(game)
            power_sum += get_game_power(outcome_dict)

        return power_sum




def main():
    start = time.time()
    game_sum = analyze_games(True)
    end = time.time()
    
    print(f"Puzzle output: {game_sum}")
    print(f"Time taken: {round(end-start, 3)} seconds")


if __name__ == "__main__":
    main()