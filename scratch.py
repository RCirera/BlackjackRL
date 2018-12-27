# For implementing RL algorithms for blackjack a few classes are necessary. Here I attempt to write them down.
#
#
# For SARSA (on-policy TD control):
#
# - Game: simulation objects that interacts with the learning player, keeps track of current state and state transition and reward for given state action pairs.
#     - dealer hand:
#     - player hand:
#
# - Player: interacts with game object. Gives an action to take for a given state
#     - Policy: dictate action to take for a given state
#     - Q table: value of state action pairs
#     -
#
#
# SARSA Algorithm:
#
# 1. Set constants:
#     - alpha: step size
#     - epsilon: e-greedy policy term
#     - gamma: discount rate, 0<=gamma<=1
#
# 2. Initialize the Q table for all state-action pairs arbitrarily except Q(terminal)=0
#
# 3. Loop for each episode:
#     1. Initialize the state S
#     2. Choose from S using a policy derived from the Q table, e.g. e-greedy
#     3. Loop for each state of the episode. While state S is not terminal:
#         1. Take action A
#         2. Observe reward R and new state S'
#         3. Choose A' from S' using a policy derived from Q, e.g. e-greedy
#         4. Update Q(S,A)=Q(S,A)+alpha[R+gamma*Q(S',A')-Q(S,A)]
#         5. Update the current state S=S'
#         6. Update the current action A=A'

from definitions import *

# game = BlackjackGame()
#
# # print(game.state())
# # print(game.dealer_hand.card_faces)
# # print(game.player_hand.card_faces)
#
# game.new_game()
#
# print(game.state())
# # print(game.dealer_hand.card_faces)
# # print(game.player_hand.card_faces)
#
# while not game.game_over and game.player_count < 17:
#     game.hit()
#
# print(game.state())
# # print(game.dealer_hand.card_faces)
# # print(game.player_hand.card_faces)
#
# game.stand()
#
# print(game.state())
# print(game.dealer_hand.card_faces)
# print(game.player_hand.card_faces)

# g = BlackjackGame()
# g.new_game()
# print(g.state())
#
# while not g.game_over and g.player_count < 17:
#     g.hit()
#     print(g.state())
#
# g.stand()
# print(g.state())

qt = QTable(22, 11, 2, 2)

print(qt.entries)