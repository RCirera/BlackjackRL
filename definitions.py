import random
import numpy as np


class Card:

    def __init__(self):
        card_list = [['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'],
                     [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]]
        index = random.choice(range(0, 13))
        self.face = card_list[0][index]
        self.value = card_list[1][index]


class Hand:

    def __init__(self, size=0):
        self.cards = []
        self.card_faces = []
        self.card_values = []

        for _ in range(size):
            c = Card()
            self.cards.append(c)
            self.card_faces.append(c.face)
            self.card_values.append(c.value)

        self.value = self.count()

    def __len__(self):
        return len(self.cards)

    def empty(self):
        self.cards = []
        self.card_faces = []
        self.card_values = []
        self.value = self.count()

    def append(self, new_card):
        self.cards.append(new_card)
        self.card_faces.append(new_card.face)
        self.card_values.append(new_card.value)
        self.value = self.count()

    def count(self):
        count = sum(self.card_values)
        for ace in range(self.card_faces.count('A')):
            new_count = count + 10
            if new_count < 22:
                count = new_count
        return count

    def usable_ace(self):
        if self.card_faces.count('A') > 0 and sum(self.card_values) + 10 < 22:
            return True
        else:
            return False


class BlackjackGame:

    def __init__(self):
        self.dealer_hand = Hand()
        self.player_hand = Hand()
        self.dealer_count = self.dealer_hand.count()
        self.player_count = self.player_hand.count()
        self.player_usable_ace = self.player_hand.usable_ace()
        self.game_over = False

    def state(self):
        return self.dealer_count, self.player_count, self.player_usable_ace

    def new_game(self):
        self.dealer_hand = Hand(1)
        self.player_hand = Hand(2)
        self.dealer_count = self.dealer_hand.count()
        self.player_count = self.player_hand.count()
        self.player_usable_ace = self.player_hand.usable_ace()
        self.game_over = False

    def hit(self):
        if not self.game_over:
            self.player_hand.append(Card())
            self.player_count = self.player_hand.count()
            self.player_usable_ace = self.player_hand.usable_ace()
            if self.check_player_bust():
                self.game_over = True
                print("Player Busted! Dealer Wins!")

    def stand(self):
        if not self.game_over:
            while self.dealer_count < 17:
                self.dealer_hand.append(Card())
                self.dealer_count = self.dealer_hand.count()
            self.game_over = True
            self.check_game_state()

    def check_player_bust(self):
        if self.player_count > 21:
            return True
        else:
            return False

    def check_game_state(self):
        if self.dealer_count > 21:
            print("Dealer Busted! Player Wins")
        elif self.player_count > self.dealer_count:
            print("Player Wins")
        elif self.player_count == self.dealer_count:
            print("Tie!")
        else:
            print("Dealer Wins!")


class QTable:

    def __init__(self, dims):
        self.entries = np.zeros(dims, dtype=int)
