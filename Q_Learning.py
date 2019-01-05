# Q-Learning Algorithm:
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
#         3. Choose A' from S' to maximize Q(S',A')
#         4. Update Q(S,A)=Q(S,A)+alpha[R+gamma*Q(S',A')-Q(S,A)]
#         5. Update the current state S=S'
#         6. Update the current action A=A'


from definitions import *


# Set constants
alpha = 0.1  # step size
epsilon = 0.7  # e-greedy policy term
gamma = 0.1  # discount rate
episodes = 100000  # number of episodes to run
test_episodes = 100000  # number of test episodes to run after training

# Initialize the learner
learner = BlackjackLearner()

# Run for many episodes
for episode in range(1, episodes):

    # Initialize the game
    game = BlackjackGame()

    # New episode
    game.new_game()

    while not game.game_over:

        # Get the state
        state = game.state()

        # Choose action from e-greedy
        action = learner.e_greedy_action(state, epsilon)

        # Get state-action value
        state_action_value = learner.get_value(state, action)

        # Take action and get reward
        reward = game.act(action)

        # Get new state
        new_state = game.state()

        # Get new action
        new_action = learner.greedy_action(new_state)

        # Get new state-action value
        new_state_action_value = learner.get_value(new_state, new_action)

        # Update the state-action value table
        updated_state_action_value = state_action_value \
                                     + alpha * (reward + gamma * new_state_action_value - state_action_value)
        learner.set_value(state, action, updated_state_action_value)

        # Display training updates
        if episode % 10000 == 0:
            print("%.2f of training complete." % (episode / episodes * 100))
            learner.save("./Saved Learners/Q_Learning.p")
            # learner.test(10000)

# Save the learner
learner.save("./Saved Learners/Q_Learning.p")

# Test the learned optimal policy
learner.test(test_episodes)
