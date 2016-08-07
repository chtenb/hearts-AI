from card import Suit, Rank, Card, Deck


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

    def are_hearts_broken(self):
        for cards in self._cards_taken:
            if any(card.suit == Suit.hearts for card in cards):
                return True
        return False

    def is_trick_valid(self, trick):
        return True  # TODO: implement this

    def say(self, message):
        if self.verbose:
            print(message)

    def play(self):
        """
        Simulate a game and return a 4-tuple of the scores.
        """
        # Players and their hands are indentified by indices ranging from 0 to 4

        # Perform the card passing
        for i in range(4):
            for card in self.players[i].pass_cards(self._player_hands[i]):
                self._player_hands[i].remove(card)
                self._player_hands[(i + 1) % 4].append(card)

        # Play the tricks
        leading_index = self.player_index_with_two_of_clubs()
        for _ in range(13):
            leading_index = self.play_trick(leading_index)

        # Print and return the results
        self.say('Results:')
        for i in range(4):
            self.say('Player {}: {} from {}'.format(i,
                                                 self.count_points(self._cards_taken[i]),
                                                 ' '.join(str(card) for card in self._cards_taken[i])),
                  )

        return tuple(self.count_points(self._cards_taken[i]) for i in range(4))

    def play_trick(self, leading_index):
        player_index = leading_index
        trick = []
        for _ in range(4):
            played_card = self.players[player_index].play_card(
                self._player_hands[player_index], trick, self.are_hearts_broken())
            trick.append(played_card)
            if not self.is_trick_valid(trick):
                raise ValueError('Player {} played an invalid card: {}. Resulting trick: {}'
                                 .format(player_index, played_card, trick))
            self._player_hands[player_index].remove(played_card)
            player_index = (player_index + 1) % 4

        self.say('Trick: {}'.format(trick))
        winning_index = self.winning_index(trick)
        winning_player_index = (leading_index + winning_index) % 4
        self.say('Winning player: {}'.format(winning_player_index))
        self._cards_taken[winning_player_index].extend(trick)
        return winning_player_index

    def player_index_with_two_of_clubs(self):
        two_of_clubs = Card(Suit.clubs, Rank.two)
        for i in range(4):
            if two_of_clubs in self._player_hands[i]:
                return i

        raise AssertionError('No one has the two of clubs. This should not happen.')

    def winning_index(self, trick):
        leading_suit = trick[0].suit

        result = 0
        result_rank = Rank.two
        for i, card in enumerate(trick):
            if card.suit == leading_suit and card.rank > result_rank:
                result = i
                result_rank = card.rank

        return result

    def count_points(self, cards):
        queen_of_spades = Card(Suit.spades, Rank.queen)
        result = 0
        for card in cards:
            if card.suit == Suit.hearts:
                result += 1
            elif card == queen_of_spades:
                result += 13
        return result
