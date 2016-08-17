"""This module containts the abstract class Player and some implementations."""
from random import shuffle

from card import Suit, Rank, Card, Deck
from rules import is_card_valid


class Player:

    """
    Abstract class defining the interface of a Computer Player.
    """

    def pass_cards(self, hand):
        """Must return a list of three cards from the given hand."""
        return NotImplemented

    def play_card(self, hand, trick, trick_nr, are_hearts_broken):
        """
        Must return a card from the given hand.
        trick is a list of cards played so far.
        trick can thus have 0, 1, 2, or 3 elements.
        are_hearts_broken is a boolean indicating whether the hearts are broken yet.
        trick_nr is an integer indicating the current trick number, starting with 0.
        """
        return NotImplemented


class StupidPlayer(Player):

    """
    Most simple player you can think of.
    It just plays random valid cards.
    """

    def pass_cards(self, hand):
        return hand[:3]

    def play_card(self, hand, trick, trick_nr, are_hearts_broken):
        # Play first card that is valid
        for card in hand:
            if is_card_valid(hand, trick, card, trick_nr, are_hearts_broken):
                return card
        raise AssertionError(
            'Apparently there is no valid card that can be played. This should not happen.'
        )


class SimplePlayer(Player):

    """
    This player has a notion of a card being undesirable.
    It will try to get rid of the most undesirable cards while trying not to win a trick.
    """

    def __init__(self, verbose=False):
        self.verbose = verbose
        if verbose:
            deck = Deck()
            deck.cards.sort(key=self.undesirability)
            self.say('Card undesirability: ')
            for card in deck.cards:
                self.say('{}: {}', card, self.undesirability(card))

    def say(self, message, *formatargs):
        if self.verbose:
            print(message.format(*formatargs))

    def undesirability(self, card):
        return (
            card.rank.value
            + (10 if card.suit == Suit.spades and card.rank >= Rank.queen else 0)
        )

    def pass_cards(self, hand):
        hand.sort(key=self.undesirability, reverse=True)
        return hand[:3]

    def play_card(self, hand, trick, trick_nr, are_hearts_broken):
        # Lead with a low card
        if not trick:
            hand.sort(key=lambda card:
                      100 if not are_hearts_broken and card.suit == Suit.hearts else
                      card.rank.value)
            return hand[0]

        hand.sort(key=self.undesirability, reverse=True)
        self.say('Hand: {}', hand)
        self.say('Trick so far: {}', trick)

        # Safe cards are cards which will not result in winning the trick
        leading_suit = trick[0].suit
        max_rank_in_leading_suit = max([card.rank for card in trick
                                        if card.suit == leading_suit])
        valid_cards = [card for card in hand
                       if is_card_valid(hand, trick, card, trick_nr, are_hearts_broken)]
        safe_cards = [card for card in valid_cards
                      if card.suit != leading_suit or card.rank <= max_rank_in_leading_suit]

        self.say('Valid cards: {}', valid_cards)
        self.say('Safe cards: {}', safe_cards)

        try:
            return safe_cards[0]
        except IndexError:
            queen_of_spades = Card(Suit.spades, Rank.queen)
            # Don't try to take a trick by laying the queen of spades
            if valid_cards[0] == queen_of_spades and len(valid_cards) > 1:
                return valid_cards[1]
            else:
                return valid_cards[0]

