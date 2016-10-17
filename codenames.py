# codenames imitation

import pandas as pd
import pickle as p
import random
import re


class Player():
    def __init__(self, spy_type=None, team=None):
        self.spy_type = spy_type  # spy or spymaster
        self.team = team  # RED or BLUE


class Tile():
    def __init__(self, value):
        self.value = value
        self.card_type = 'blank'
        self.actual = 'blank'

    def update_type(self, classification):
        self.card_type = classification

    def assign_actual(self):
        self.actual = self.value


def board():
    f = open('dictionary.txt', 'r')
    words = []
    for word in f:
        word = word.strip()
        word = word.lower()
        words.append(word)

    dictionary = random.sample(words, 25)

    tiles = []
    [tiles.append(Tile(i)) for i in dictionary]

    for i in range(0, 7):
        tiles[i].update_type('RED')
    for j in range(7, 13):
        tiles[j].update_type('BLUE')
    for k in range(13, 24):
        tiles[k].update_type('neutral')
    tiles[24].update_type('GAME OVER')

    # shuffle the elements so they aren't always in the same order
    random.shuffle(tiles)

    return tiles


def garner_prompt(team):
    raw_inputs = input('\n' + team + ' Spymaster, please enter your hint and a number in the form \'hint; number\'.\n').strip()
    splt_str = re.split('\W+', raw_inputs)
    if len(splt_str) != 2:
        print('\nPlease enter a valid hint.')
        return garner_prompt(team)
    else:
        return splt_str


def garner_guess(idx, tiles):
    # find all of the tile names to check if the guess is valid
    tile_names = []
    [tile_names.append(card.value) for card in tiles]

    guess = input('Spy, please enter guess ' + str(idx + 1) + ' (type \'pass\' to end).\n').strip()

    if guess.lower() == 'pass':
        return (guess, 0)
    elif guess not in tile_names:
        print('\nPlease enter a valid guess.')
        return garner_guess(idx, tiles)
    else:
        idx2 = tile_names.index(guess)
        if tiles[idx2].actual == 'blank':
            return (guess, idx2)
        else:
            print('\nThat word has already been guessed. Please choose another.')
            return garner_guess(idx, tiles)


def make_guess(idx, team, other_team, tiles, maximum, scoreboard, max_scores):
    if idx >= maximum:
        return 'other'

    guess, dict_idx = garner_guess(idx, tiles)

    if guess == 'pass':
        return 'other'
    elif tiles[dict_idx].card_type == other_team:
        scoreboard[other_team] += 1
        tiles[dict_idx].assign_actual()
        # update appearance of tile
        return 'other'
    elif tiles[dict_idx].card_type == 'neutral':
        tiles[dict_idx].assign_actual()
        # update appearance of tile
        return 'other'
    elif tiles[dict_idx].card_type == 'GAME OVER':
        tiles[dict_idx].assign_actual()
        return 'over'
    elif tiles[dict_idx].card_type == team:
        scoreboard[team] += 1
        if scoreboard[team] >= max_scores[team]:
            return 'other'
        tiles[dict_idx].assign_actual()
        return make_guess(idx+1, team, other_team, tiles, maximum, scoreboard, max_scores)


def turn(team, tiles, scoreboard, max_scores):
    # called every time a turn ends whether because the guesses are exhausted
    # or a bad guess was made

    print('\n********************', scoreboard, '******************')

    # check for victory
    if scoreboard['RED'] >= max_scores['RED']:
        return 'RED team wins!'
    if scoreboard['BLUE'] >= max_scores['BLUE']:
        return 'BLUE team wins!'

    # define the other team
    if team == 'RED':
        other_team = 'BLUE'
    elif team == 'BLUE':
        other_team = 'RED'
    else:
        raise NameError('Pass a team name to the turn.')

    hint, number = garner_prompt(team)
    hint = hint.lower()
    number = int(number)

    status = make_guess(idx=0,
                        team=team,
                        other_team=other_team,
                        tiles=tiles,
                        maximum=number+1,
                        scoreboard=scoreboard,
                        max_scores=max_scores)

    if status == 'other':
        return turn(other_team, tiles, scoreboard, max_scores)
    elif status == 'over':
        return other_team + ' team wins!\n'


if __name__ == '__main__':
    board = board()

    max_scores = {'RED': 0, 'BLUE': 0}
    for tile in board:
        if tile.card_type == 'RED':
            max_scores['RED'] += 1
        elif tile.card_type == 'BLUE':
            max_scores['BLUE'] += 1
        else:
            continue

    score = {'RED': 0, 'BLUE': 0}

    for i in board:
        print(i.value, i.card_type)

    print(turn(team='RED', tiles=board, scoreboard=score, max_scores=max_scores))
