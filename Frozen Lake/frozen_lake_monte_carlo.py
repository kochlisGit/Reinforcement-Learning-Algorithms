import random as rand
import time
import matplotlib.pyplot as plt

UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

class Lake:
    def __init__(self, width, height, goals, holes, barriers, initial_state):
        self.env_dict = {0: '.', 1: '*', 2: 'G', 3: 'O', 4: 'X'}

        self.width = width
        self.height = height
        self.num_of_states = width*height
        self.goals = goals
        self.barriers = barriers
        self.holes = holes
        self.i = initial_state[0]
        self.j = initial_state[1]
        self.ended = False
        self.winner = False
        self._construct_lake()

    def _construct_lake(self):
        self.lake_grid = [ [ 0 for i in range(self.width) ] for i in range(self.height) ]
        self.lake_grid[self.i][self.j] = 1
        for goal in self.goals:
            i = goal[0]
            j = goal[1]
            self.lake_grid[i][j] = 2
        for hole in self.holes:
            i = hole[0]
            j = hole[1]
            self.lake_grid[i][j] = 3 
        for barrier in self.barriers:
            i = barrier[0]
            j = barrier[1]
            self.lake_grid[i][j] = 4

    def print_lake(self):
        for i in range(self.height):
            print('', '-' * 4*self.width)
            for j in range(self.width):
                print('|', self.env_dict[ self.lake_grid[i][j] ], end=' ')
            print('|')
        print('', '-' * 4*self.width, '\n')

    def is_valid(self, i, j):
        return i >= 0 and i < self.height and j >=0 and j < self.width and (i,j) not in self.barriers

    def move(self, i, j):
        self.i = i
        self.j = j
        self._construct_lake()

    def undo_move(self, movement):
        if movement == UP:
            self.i +=1
        elif movement == DOWN:
            self.i -= 1
        elif movement == LEFT:
            self.j += 1
        elif movement == RIGHT:
            self.j -= 1
        self._construct_lake()

    def game_over(self):
        if (self.i, self.j) in self.holes:
            self.ended = True
        else:
            if (self.i, self.j) in self.goals:
                self.ended = True
                self.winner = True

    def is_goal(self, i, j):
        return (i,j) in self.goals

    def _go_up(self):
        return self.i-1, self.j

    def _go_down(self):
        return self.i+1, self.j

    def _go_left(self):
        return self.i, self.j-1

    def _go_right(self):
        return self.i, self.j+1

    def generate_actions(self):
        actions = []

        i, j = self._go_up()
        if self.is_valid(i, j):
            actions.append( (i,j, UP) )
        i, j = self._go_down()
        if self.is_valid(i, j):
            actions.append( (i,j, DOWN) )
        i, j = self._go_left()
        if self.is_valid(i, j):
            actions.append( (i,j, LEFT) )
        i, j = self._go_right()
        if self.is_valid(i, j):
            actions.append( (i,j, RIGHT) )
        return actions

    def generate_state_id(self):
        return self.i * self.width + self.j

    def get_reward(self):
        if self.winner:
            return 1
        elif self.ended:
            return -1
        else:
            return 0.5

class Agent:
    def __init__(self, epsilon, gamma, value_function):
        self.epsilon = epsilon
        self.gamma = gamma
        self.value_function = value_function
        self.state_history = []

    def set_epsilon(self, epsilon):
        self.epsilon = epsilon

    def reset_state_history(self):
        self.state_history = []

    def play(self, env):
        actions = env.generate_actions()
        p = rand.uniform(0.0, 1.0)
        next_action = ()
        if p < self.epsilon:
            next_action = rand.choice(actions)
        else:
            best_action_value = -1
            for action in actions:
                i = action[0]
                j = action[1]
                movement = action[2]
                if env.is_valid(i, j):
                    env.move(i, j)
                    state_id = env.generate_state_id()
                    env.undo_move(movement)
                    if self.value_function[state_id] > best_action_value:
                        best_action_value = self.value_function[state_id]
                        next_action = (i, j)
        i = next_action[0]
        j = next_action[1]
        env.move(i, j)

    def update_state_history(self, state_id):
        self.state_history.append(state_id)

    # Monte-Carlo update.
    def update(self, env):
        reward = env.get_reward()
        target = reward
        for state_id in reversed(self.state_history):
            value = self.value_function[state_id] + self.gamma*( target - self.value_function[state_id] )
            self.value_function[state_id] = value
            target = value
        self.reset_state_history()

def construct_lake():
    width = 6
    height = 6
    goals = { (0,3), (3,5) }
    holes = { (0,4), (0,5), (2,5), (3,4), (2,4), (4,0), (5,2) }
    barriers = { (3,3), (4,4) }
    initial_state = (5, 0)
    return Lake(width, height, goals, holes, barriers, initial_state)

def generate_value_function(lake):
    value_function = [0] * lake.num_of_states

    for goal in lake.goals:
        i = goal[0]
        j = goal[1]
        lake.move(i, j)
        state_id = lake.generate_state_id()
        value_function[state_id] = 1
    for hole in lake.holes:
        i = hole[0]
        j = hole[1]
        lake.move(i, j)
        state_id = lake.generate_state_id()
        value_function[state_id] = -1
    return value_function

def play_game(agent, env, show_lake=False):
    steps = 0

    while not env.ended:
        steps += 1

        if show_lake:
            env.print_lake()
            time.sleep(1)
        agent.play(env)

        env.game_over()

        state_id = env.generate_state_id()
        agent.update_state_history(state_id)

    agent.update(env)
    return steps

def train(epsilon = 0.1, gamma = 0.5, test_agent=False):
    value_function = generate_value_function( construct_lake() )
    agent = Agent(epsilon, gamma, value_function)
    num_of_episodes = 50
    episodes_steps = [0]*num_of_episodes

    print('Training...')

    for e in range(num_of_episodes):
        agent.set_epsilon( 1/(1+e) )
        steps = play_game(agent, construct_lake(), show_lake=False)
        episodes_steps[e] = steps

    if test_agent:
        print('Testing')
        print(agent.value_function)

        plt.plot(episodes_steps)
        plt.show()

        agent.set_epsilon(0.0)
        play_game(agent, construct_lake(), show_lake=True)

    return episodes_steps