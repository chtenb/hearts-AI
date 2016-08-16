"""
This module contains a few functions comprising the rules of the game.
"""

from card import Suit

def is_card_valid(hand, trick, card, are_hearts_broken):
    """
    Return True if the given card is valid to play in given context, False otherwise.
    """
    # TODO: implement points are forbidden in first trick
    if not trick:
        return are_hearts_broken or (
            not are_hearts_broken and (card.suit != Suit.hearts
                                       or all([card.suit == Suit.hearts for card in hand]))
        )

    leading_suit = trick[0].suit
    return card.suit == leading_suit or all([card.suit != leading_suit for card in hand])

