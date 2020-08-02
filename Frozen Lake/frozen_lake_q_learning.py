import numpy as np
import time
import matplotlib.pyplot as plt

# Defining lake's Width & Height.
height = 6
width = 6

# Defining agent's actions.
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

# Defining enviroment objets.
PATH = 0
AGENT = 1
HOLE = 2
GOAL = 3

num_of_states = height*width
num_of_actions = 4

# Lake is the Enviroment class. It adds objects to the lake and rewards the agent.
class Lake:
    def __init__(self, agent, holes, goals):
        self.lake_dict = {PATH: '.', AGENT: '*', HOLE: 'O', GOAL: 'G'}
        self.agent = agent
        self.holes = holes
        self.goals = goals

        self._update_lake()

    # Reconstructs - Updates the enviroment every time a change happens.
    def _update_lake(self):
        self.lake = np.zeros( shape=(height, width) )
        self.lake[ self.agent[0] ][ self.agent[1] ] = AGENT
        for hole in self.holes:
            self.lake[ hole[0] ][ hole[1] ] = HOLE
        for goal in self.goals:
            self.lake[ goal[0] ][ goal[1] ] = GOAL

    # Prints the lake's grid, which contains the paths, the agent, the holes and the goals.
    def print_lake(self):
        print('', '-' * 4*width)
        for i in range(height):
            for j in range(width):
                print('|', self.lake_dict[ self.lake[i][j] ], end=' ')
            print('|')
        print('', '-' * 4*width, '\n')

    # Checks whether an agent's action is valid.
    def valid_action(self, action):
        if action == UP:
            return self.agent[0] - 1 >= 0
        elif action == DOWN:
            return self.agent[0] + 1 < height
        elif action == LEFT:
            return self.agent[1] - 1 >= 0
        elif action == RIGHT:
            return self.agent[1] + 1 < width

    # Moves the agent based on his action.
    def move_agent(self, action):
        if action == UP:
            self.agent[0] -= 1
        elif action == DOWN:
            self.agent[0] += 1
        elif action == LEFT:
            self.agent[1] -= 1
        elif action == RIGHT:
            self.agent[1] += 1
        self._update_lake()

    # Checks whether the agent visited a terminal (goal) state.
    def game_over(self):
        return self.agent in self.goals

    # Generates all possible actions of the agent. An action is possible if it is a valid one.
    def generate_possible_actions(self):
        possible_actions = []
        for action in range(4):
            if self.valid_action(action):
                possible_actions.append(action)
        return possible_actions

    # Gets the state of the enviroment, based on the agent's position.
    def get_state(self):
        return self.agent[0]*width + self.agent[1]

    # Rewards the agent 10 points if he visited a terminal state, -10 if he visited trap, otherwise 1.
    def get_reward(self):
        if self.game_over():
            return 10
        else:
            if self.agent in self.holes:
                return -10
            else:
                return 1

# The agent's class. Contains methods for exploring and exploiting the states in the enviroment.
class Agent:
    def __init__(self, epsilon, gamma, alpha):
        self.epsilon = epsilon
        self.gamma = gamma
        self.alpha = alpha
        self.Q = np.zeros( shape=(num_of_states, num_of_actions), dtype=np.float32 )
        self.state_history = []

    # Prints the Q-Function.
    def print_Q_function(self):
        print(self.Q)

    # Sets epsilon. Epsilon is 0.1 by default, but i optimize it at the start of an episode.
    def set_epsilon(self, epsilon):
        self.epsilon = epsilon

    # Adds the last visited state to agent's memory.
    def update_state_history(self, state):
        self.state_history.append(state)

    # Resets the state history.
    def reset_state_history(self):
        self.state_history = []

    # Takes action, using the modified epsilon greedy algorithm.
    # e = 1/i, where i is the i-th episode.
    # It explores the enviroment with probability e.
    # It exploits the highest rewarding action with probability 1-e.
    def take_action(self, lake):
        possible_actions = lake.generate_possible_actions()
        next_action = -1
        p = np.random.uniform(low=0.0, high=1.0)
        if p < self.epsilon:
            next_action = np.random.choice(possible_actions)
        else:
            state = lake.get_state()
            highest_reward = - 1
            for action in range(4):
                if action in possible_actions and self.Q[state][action] > highest_reward:
                    highest_reward = self.Q[state][action]
                    next_action = action
        return next_action

    # Updates the Q-Function. Q(state, action) = Q(state, action) + alpha * (reward + gamma * Q'(state', action') - Q(state, action) )
    def update(self, reward, action, new_state):
        state = self.state_history[-1]
        target = reward + self.gamma*np.max( self.Q[new_state] )
        self.Q[state][action] += self.alpha * ( target - self.Q[state][action] )

# Constructs the lake's enviroment. It returns a lake with the agent, the holes and the goals.
def construct_lake():
    agent = [5,0]
    holes = [ [0,4], [0,5], [2,5], [3,4], [2,4], [4,0], [5,2] ]
    goals = [ [0,3], [3,5] ]
    return Lake(agent, holes, goals)

# The agent plays the game over and over again.
# 1. Check whether it's game over.
# 2. Agent makes a move.
# 3. Agent receives a reward.
# 4. Agent updates the Q Function (Q-Learning).
def play_game(agent, lake, show_lake=False):
    steps = 0

    if show_lake:
        agent.print_Q_function()

    agent.update_state_history( lake.get_state() )
    while not lake.game_over():
        steps += 1
        action = agent.take_action(lake)
        lake.move_agent(action)

        new_state = lake.get_state()
        reward = lake.get_reward()
        agent.update(reward, action, new_state)
        agent.update_state_history(new_state)

        if show_lake:
            lake.print_lake()
            time.sleep(1)

    agent.reset_state_history()
    return steps

def train(epsilon=0.1, gamma=0.3, alpha=0.7, test_agent=False):
    agent = Agent(epsilon, gamma, alpha)
    num_of_episodes = 50
    episode_steps = [0]*num_of_episodes

    print('Training...')

    for e in range(num_of_episodes):
        agent.set_epsilon( 1/(1+e) )
        steps = play_game(agent, construct_lake(), show_lake=False)
        episode_steps[e] = steps

    if test_agent:
        print('Testing...')

        plt.plot(episode_steps)
        plt.show()

        agent.set_epsilon(0)
        play_game(agent, construct_lake(), show_lake=True)

    return episode_steps
