"""
This module contains the definition of types fundamental to card games,
most notably the type Card.
"""

import sys
from random import shuffle

from orderedenum import OrderedEnum


class Suit(OrderedEnum):

    clubs = 0
    diamonds = 1
    spades = 2
    hearts = 3

    def __repr__(self):
        if sys.stdout.encoding in ['cp437', 'cp850']:
            # These are the correct unicode symbols in cp437 or cp850 encoding
            # They don't work for 1252 of utf8
            return [chr(5), chr(4), chr(6), chr(3)][self.value]
        else:
            return [' of clubs', ' of diamonds', ' of spades', ' of hearts'][self.value]


class Rank(OrderedEnum):

    two = 2
    three = 3
    four = 4
    five = 5
    six = 6
    seven = 7
    eight = 8
    nine = 9
    ten = 10
    jack = 11
    queen = 12
    king = 13
    ace = 14

    def __repr__(self):
        if self.value <= 10:
            return str(self.value)
        else:
            return ['J', 'Q', 'K', 'A'][self.value - 11]


class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __repr__(self):
        return repr(self.rank) + repr(self.suit)

    def __lt__(self, other):
        return (self.suit, self.rank) < (other.suit, other.rank)

    def __eq__(self, other):
        return (self.suit, self.rank) == (other.suit, other.rank)


class Deck:

    def __init__(self):
        self.cards = [Card(suit, rank) for suit in Suit for rank in Rank]

    def deal(self):
        """
        Shuffles the cards and returns 4 lists of 13 cards.
        """
        shuffle(self.cards)
        for i in range(0, 52, 13):
            yield sorted(self.cards[i:i + 13])
