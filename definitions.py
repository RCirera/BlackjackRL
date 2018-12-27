import random
import numpy as np
import warnings


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
            return 1
        else:
            return 0


class BlackjackGame:

    def __init__(self, verbose=False):
        self.dealer_hand = Hand()
        self.player_hand = Hand()
        self.dealer_count = self.dealer_hand.count()
        self.player_count = self.player_hand.count()
        self.player_usable_ace = self.player_hand.usable_ace()
        self.game_over = False
        self.verbose = verbose

    def state(self):
        return [self.dealer_count, self.player_count, self.player_usable_ace]

    def new_game(self):
        self.dealer_hand = Hand(1)
        self.player_hand = Hand(2)
        self.dealer_count = self.dealer_hand.count()
        self.player_count = self.player_hand.count()
        self.player_usable_ace = self.player_hand.usable_ace()
        self.game_over = False

    def act(self, action):
        if action == 0:
            reward = self.stand()
            return reward
        elif action == 1:
            reward = self.hit()
            return reward
        else:
            return

    def hit(self):
        if not self.game_over:
            self.player_hand.append(Card())
            self.player_count = self.player_hand.count()
            self.player_usable_ace = self.player_hand.usable_ace()
            if self.check_player_bust():
                self.game_over = True
                if self.verbose:
                    print("Player Busted! Dealer Wins!")
                reward = -1
                return reward
            else:
                reward = 0
                return reward

    def stand(self):
        if not self.game_over:
            while self.dealer_count < 17:
                self.dealer_hand.append(Card())
                self.dealer_count = self.dealer_hand.count()
            self.game_over = True
            reward = self.check_game_state()
            return reward

    def check_player_bust(self):
        if self.player_count > 21:
            return True
        else:
            return False

    def check_game_state(self):
        if self.dealer_count > 21:
            if self.verbose:
                print("Dealer Busted! Player Wins")
            reward = 1
            return reward
        elif self.player_count > self.dealer_count:
            if self.verbose:
                print("Player Wins")
            reward = 1
            return reward
        elif self.player_count == self.dealer_count:
            if self.verbose:
                print("Tie!")
            reward = 0
            return reward
        else:
            if self.verbose:
                print("Dealer Wins!")
            reward = -1
            return reward


class BlackjackLearner:

    def __init__(self, dims=(32, 32, 2, 2)):
        self.q_table = np.zeros(dims, dtype=float)

    def set_value(self, state, action, value):
        # print(self.q_table[state[0], state[1], state[2], action])
        self.q_table[state[0], state[1], state[2], action] = value
        # print(value)
        # print(self.q_table[state[0], state[1], state[2], action])
        return

    def get_value(self, state, action):
        value = self.q_table[state[0], state[1], state[2], action]
        return value

    def greedy_action(self, state):
        state_action_values = self.q_table[state[0], state[1], state[2], :]
        max_value = max(state_action_values)
        indices = np.where(state_action_values == max_value)
        action = np.random.choice(indices[0])
        return action

    def random_action(self, state):
        state_action_values = self.q_table[state[0], state[1], state[2], :]
        random_value = np.random.choice(state_action_values)
        indices = np.where(state_action_values == random_value)
        action = np.random.choice(indices[0])
        return action

    def e_greedy_action(self, state, e=0.5):
        if np.random.ranf() < 1-e:
            return self.greedy_action(state)
        else:
            return self.random_action(state)

    def test(self, episodes):
        player_wins = 0
        player_ties = 0
        player_losses = 0

        for episode in range(1, episodes):
            game = BlackjackGame()
            game.new_game()

            while not game.game_over:
                state = game.state()
                action = self.greedy_action(state)
                reward = game.act(action)

                if game.game_over:
                    if reward == 1:
                        player_wins += 1
                    elif reward == 0:
                        player_ties += 1
                    elif reward == -1:
                        player_losses += 1
                    else:
                        warnings.warn("No reward received at game over.")

        print("Percentage of Wins: %.2f" % (player_wins/episodes * 100))
        print("Percentage of Ties: %.2f" % (player_ties/episodes * 100))
        print("Percentage of Losses: %.2f" % (player_losses/episodes * 100))
        return [player_wins, player_ties, player_losses]


