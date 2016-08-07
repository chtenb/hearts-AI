"""
This module contains the definition of types fundamental to card games,
most notably the type Card.
"""

from random import shuffle

from orderedenum import OrderedEnum


class Suit(OrderedEnum):

    clubs = 1
    diamonds = 2
    spades = 3
    hearts = 4

    def __repr__(self):
        # We assume cp437 or cp850 encoding
        return {
            1: chr(5),
            2: chr(4),
            3: chr(6),
            4: chr(3)
        }[self.value]


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
            return {
                11: 'J',
                12: 'Q',
                13: 'K',
                14: 'A'
            }[self.value]


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
        self.cards = []

        for suit in Suit:
            for rank in Rank:
                self.cards.append(Card(suit, rank))

    def deal(self):
        """
        Shuffles the cards and returns 4 lists of 13 cards.
        """
        shuffle(self.cards)
        for i in range(0, 52, 13):
            hand = self.cards[i:i + 13]
            hand.sort()
            yield hand
