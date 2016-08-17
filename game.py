from card import Suit, Rank, Card, Deck
from rules import is_card_valid, card_points


class Game:

    def __init__(self, players, verbose=False):
        """
        players is a list of four players
        """
        self.verbose = verbose
        if len(players) != 4:
            raise ValueError('There must be four players.')
        self.players = players

        # Invariant: the union of these lists makes up exactly one deck of cards
        deck = Deck()
        self._player_hands = tuple(deck.deal())
        self._cards_taken = ([], [], [], [])

    def say(self, message, *formatargs):
        if self.verbose:
            print(message.format(*formatargs))

    def are_hearts_broken(self):
        """
        Return True if the hearts are broken yet, otherwise return False.
        """
        for cards in self._cards_taken:
            if any(card.suit == Suit.hearts for card in cards):
                return True
        return False

    def play(self):
        """
        Simulate a single game and return a 4-tuple of the scores.
        """
        # Players and their hands are indentified by indices ranging from 0 till 4

        # Perform the card passing.
        # Currently always passes in one direction.
        # Alternating directions can be implemented later if desirable
        for i in range(4):
            for card in self.players[i].pass_cards(self._player_hands[i]):
                self._player_hands[i].remove(card)
                self._player_hands[(i + 1) % 4].append(card)

        # Play the tricks
        leading_index = self.player_index_with_two_of_clubs()
        for trick_nr in range(13):
            leading_index = self.play_trick(leading_index, trick_nr)

        # Print and return the results
        self.say('Results of this game:')
        for i in range(4):
            self.say('Player {} got {} points from the cards {}',
                     i,
                     self.count_points(self._cards_taken[i]),
                     ' '.join(str(card) for card in self._cards_taken[i])
                     )

        return tuple(self.count_points(self._cards_taken[i]) for i in range(4))

    def play_trick(self, leading_index, trick_nr):
        """
        Simulate a single trick.
        leading_index contains the index of the player that must begin.
        """
        player_index = leading_index
        trick = []
        are_hearts_broken = self.are_hearts_broken()
        for _ in range(4):
            player = self.players[player_index]
            player_hand = self._player_hands[player_index]
            played_card = player.play_card(player_hand, trick, trick_nr, are_hearts_broken)
            if not is_card_valid(player_hand, trick, played_card, trick_nr, are_hearts_broken):
                raise ValueError('Player {} ({}) played an invalid card {} to the trick {}.'
                                 .format(player_index, type(player).__name__, played_card, trick))
            trick.append(played_card)
            self._player_hands[player_index].remove(played_card)
            player_index = (player_index + 1) % 4

        winning_index = self.winning_index(trick)
        winning_player_index = (leading_index + winning_index) % 4
        self.say('Player {} won the trick {}.', winning_player_index, trick)
        self._cards_taken[winning_player_index].extend(trick)
        return winning_player_index

    def player_index_with_two_of_clubs(self):
        two_of_clubs = Card(Suit.clubs, Rank.two)
        for i in range(4):
            if two_of_clubs in self._player_hands[i]:
                return i

        raise AssertionError('No one has the two of clubs. This should not happen.')

    def winning_index(self, trick):
        """
        Determine the index of the card that wins the trick.
        trick is a list of four Cards, i.e. an entire trick.
        """
        leading_suit = trick[0].suit

        result = 0
        result_rank = Rank.two
        for i, card in enumerate(trick):
            if card.suit == leading_suit and card.rank > result_rank:
                result = i
                result_rank = card.rank

        return result

    def count_points(self, cards):
        """
        Count the number of points in cards, where cards is a list of Cards.
        """
        # TODO: implement "shoot the moon"
        return sum(card_points(card) for card in cards)
