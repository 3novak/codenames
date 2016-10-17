# codenames imitation

import pandas as pd
import pickle as p
import random
import re


class Player():
    # placeholder in anticipation of the ambitious goal of making this a
    # multiplayer game
    # this class is not actually functional in the current version
    def __init__(self, spy_type=None, team=None):
        self.spy_type = spy_type  # spy or spymaster
        self.team = team  # RED or BLUE


class Tile():
    # tiles are the pieces that make up the board.
    # value is drawn from the dictionary
    # card_type indicates whether the card is of type 'BLUE', 'RED',
    # 'neutral', or 'GAME OVER'. card_type is assigned when the board is first
    # created.
    # the checked attribute tracks whether the tile value has been guessed or not
    def __init__(self, value):
        self.value = value
        self.card_type = 'blank'
        self.checked = 'blank'

    def update_type(self, classification):
        # only called in the creation of the board
        self.card_type = classification

    def assign_checked(self):
        # called whenever someone guesses the corresponding value
        self.checked = self.value


def board():
    # build a board containing 25 words and their team affiliation
    # this layout remains static through the duration of the game

    # read words in from a text dictionary
    f = open('dictionary.txt', 'r')
    words = []
    for word in f:
        word = word.strip()
        word = word.lower()
        words.append(word)

    dictionary = random.sample(words, 25)

    tiles = []
    [tiles.append(Tile(i)) for i in dictionary]

    # assign team associations with the words
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
    # prompt the spymaster of the respective team for a hint and value combination
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

    # prompt the spy for a guess
    guess = input('Spy, please enter guess ' + str(idx + 1) + ' (type \'pass\' to end).\n').strip()

    if guess.lower() == 'pass':
        return (guess, 0)
    elif guess not in tile_names:
        print('\nPlease enter a valid guess.')
        return garner_guess(idx, tiles)
    else:
        # not the best order, but we check here if the tile has already been
        # guessed to prevent duplicate guesses.
        idx2 = tile_names.index(guess)
        if tiles[idx2].checked == 'blank':
            return (guess, idx2)
        else:
            print('\nThat word has already been guessed. Please choose another.')
            return garner_guess(idx, tiles)


def make_guess(idx, team, other_team, tiles, maximum, scoreboard, max_scores):
    if idx >= maximum:
        return 'other'

    guess, dict_idx = garner_guess(idx, tiles)

    # manage the outcome for each guess.
    # if the guess results in the end of the current team's turn, 'other' is
    # returned to trigger the beginning of the other_team's turn.
    if guess == 'pass':
        return 'other'
    elif tiles[dict_idx].card_type == other_team:
        scoreboard[other_team] += 1
        tiles[dict_idx].assign_checked()
        # update appearance of tile
        return 'other'
    elif tiles[dict_idx].card_type == 'neutral':
        tiles[dict_idx].assign_checked()
        # update appearance of tile
        return 'other'
    elif tiles[dict_idx].card_type == 'GAME OVER':
        # if the stop card is guessed, the game is over immediately.
        tiles[dict_idx].assign_checked()
        return 'over'
    elif tiles[dict_idx].card_type == team:
        scoreboard[team] += 1
        if scoreboard[team] >= max_scores[team]:
            return 'other'
        tiles[dict_idx].assign_checked()
        return make_guess(idx+1, team, other_team, tiles, maximum, scoreboard, max_scores)


def turn(team, tiles, scoreboard, max_scores):
    # called every time a turn ends whether because the guesses are exhausted
    # or a bad guess was made

    print('\n********************', scoreboard, '********************')

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

    # establish the outcome for a guess.
    # returned values are either
    # 1) 'other' --> other_team's turn
    # 2) 'over' --> game over because the other team guessed the stop card.
    #               (when one team guesses all of their cards, the other
    #                team's turn begins, but the score check is performed
    #                before their turn actually starts.)
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
    # initialize the 5x5 board
    board = board()

    # create the max scores and score to track points for both teams
    max_scores = {'RED': 0, 'BLUE': 0}
    for tile in board:
        if tile.card_type == 'RED':
            max_scores['RED'] += 1
        elif tile.card_type == 'BLUE':
            max_scores['BLUE'] += 1
        else:
            continue

    score = {'RED': 0, 'BLUE': 0}

    # while we are still developing, this provides a master view of the board
    # including which words are in play and each word's affilation.
    for i in board:
        print(i.value, i.card_type)

    # let the games begin! begins the game and prints the outcome.
    print(turn(team='RED', tiles=board, scoreboard=score, max_scores=max_scores))

    # todo: add a help command
