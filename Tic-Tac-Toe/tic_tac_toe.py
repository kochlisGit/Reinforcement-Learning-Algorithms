import random as rand

num_of_states = 3**9

class Enviroment:
    def __init__(self):
        self.pieces = {0 : ' ', 1 : 'O', 2 : 'X'}
        self.board = [ [0, 0, 0],
                        [0, 0, 0],
                        [0, 0, 0] ]
        self.winner = None
        self.ended = False

    # Prints the board.
    def print_board(self):
        print('    0   1   2')
        print('  --------------')
        print('0 |', self.pieces[ self.board[0][0] ], '|', self.pieces[ self.board[0][1] ], '|', self.pieces[ self.board[0][2] ], '|')
        print('  --------------')
        print('1 |', self.pieces[ self.board[1][0] ], '|', self.pieces[ self.board[1][1] ], '|', self.pieces[ self.board[1][2] ], '|')
        print('  --------------')
        print('2 |', self.pieces[ self.board[2][0] ], '|', self.pieces[ self.board[2][1] ], '|', self.pieces[ self.board[2][2] ], '|')
        print('  --------------\n')

    # Checks if Board[i][j] is empty.
    def is_empty(self, i, j):
        return self.board[i][j] == 0

    # Puts a piece at Board[i][j].
    def put_piece(self, i, j, p):
        self.board[i][j] = p

    def _check_rows(self):
        for i in range(3):
            p = self.board[i][0]
            if p != 0 and self.board[i][0] == self.board[i][1] == self.board[i][2]:
                self.winner = p
                self.ended = True
                break

    def _check_columns(self):
        for j in range(3):
            p = self.board[0][j]
            if p != 0 and self.board[0][j] == self.board[1][j] == self.board[2][j]:
                self.winner = p
                self.ended = True
                break

    def _check_diagonals(self):
        p = self.board[0][0]
        if p != 0 and self.board[0][0] == self.board[1][1] == self.board[2][2]:
            self.winner = p
            self.ended = True
        p = self.board[0][2]
        if p != 0 and self.board[0][2] == self.board[1][1] == self.board[2][0]:
            self.winner = p
            self.ended = True

    # Checks if the game is over. # First it checks rows, then columns, then diagonals and finally if it is drawn.
    def game_over(self):
        self._check_rows()
        if self.winner == None:
            self._check_columns()
            if self.winner == None:
                self._check_diagonals()
                if self.winner == None:
                    self.ended = True
                    for i in range(3):
                        for j in range(3):
                            if self.board[i][j] == 0:
                                self.ended = False
                                return

    # Generates the state of the game (0 - 19683)
    def generate_game_state(self):
        state_id = 0
        k = 0
        for i in range(3):
            for j in range(3):
                v = self.board[i][j]
                state_id += (3**k)*v
                k += 1
        return state_id

    # Rewards the agent with the winning piece.
    def get_reward(self, p):
        if self.ended:
            if self.winner == p:
                return 1
            else:
                return 0
        else:
            return 0

class Human:
    def __init__(self, p):
        self.piece = p

    def play(self, env):
        i = 0
        j = 0
        while True:
            i, j = map( int, input('Enter a square (i j) from range [0, 2]: ').split() )
            if i > -1 and i < 3 and j > -1 and j < 3 and env.is_empty(i, j):
                break
            else:
                print('Invalid move. Try again.')
        env.put_piece(i, j, self.piece)

    def update_state_history(self, state_id):
        pass

    def update(self, env):
        pass

class Agent:
    def __init__(self, p, epsilon, learn_rate, value_function, verbose):
        self.piece = p
        self.epsilon = epsilon
        self.learn_rate = learn_rate
        self.value_function = value_function
        self.state_history = []
        self.verbose = verbose

    def set_epsilon(self, epsilon):
        self.epsilon = epsilon

    def set_verbose(self, verbose):
        self.verbose = verbose

    def reset_state_history(self):
        self.state_history = []

    # Agents explores with Probability = epsilon or Exploits the state with the highest value.
    def play(self, env):
        p = rand.uniform(0.0, 1.0)
        next_move = None
        if p < self.epsilon:
            if self.verbose:
                print('Taking a random Action (Exploring)')

            possible_moves = []
            for i in range(3):
                for j in range(3):
                    if env.is_empty(i, j):
                        possible_moves.append( (i, j) )
            next_move = rand.choice(possible_moves)
        else:
            if self.verbose:
                print('Taking a greedy Action (Exploiting)')

            best_value = -1.
            for i in range(3):
                for j in range(3):
                    if env.is_empty(i, j):
                        env.put_piece(i, j, self.piece)
                        state_id = env.generate_game_state()
                        env.put_piece(i, j, 0)
                        if self.value_function[state_id] > best_value:
                            best_value = self.value_function[state_id]
                            next_move = (i, j)

        i = next_move[0]
        j = next_move[1]
        env.put_piece(i, j, self.piece)

    # Updates state history, so that agent remembers every state during an episode.
    def update_state_history(self, state_id):
        self.state_history.append(state_id)

    # Rewards the agent based on the states and final result.
    def update(self, env):
        reward = env.get_reward(self.piece)
        target = reward
        for state_id in reversed(self.state_history):
            value = self.value_function[state_id] + self.learn_rate*( target - self.value_function[state_id] )
            self.value_function[state_id] = value
            target = value
        self.reset_state_history()

# Generates all possible states for both players.
def generate_possible_states(env, i=0, j=0):
    possible_states = []

    for p in env.pieces:
        if env.is_empty(i, j):
            env.put_piece(i, j, p)
        if j != 2:
            possible_states += generate_possible_states(env, i, j+1)
        else:
            if i != 2:
                possible_states += generate_possible_states(env, i+1, 0)
            else:
                env.game_over()
                state_id = env.generate_game_state()
                possible_states.append( (state_id, env.winner, env.ended) )
    return possible_states

# Generate Value Function based on agent's piece.
def generate_value_function(possible_states, p):
    value_function = [0.5]*num_of_states
    for state in possible_states:
        state_id = state[0]
        winner = state[1]
        ended = state[2]
        if ended:
            if winner == p:
                value_function[state_id] = 1
            else:
                value_function[state_id] = 0
    return value_function

def play_game(p1, p2, env, show_board=False):
    current_player = None
    while not env.ended:
        if current_player == p1:
            current_player = p2
        else:
            current_player = p1

        if show_board:
            env.print_board()
        current_player.play(env)

        env.game_over()

        state_id = env.generate_game_state()
        p1.update_state_history(state_id)
        p2.update_state_history(state_id)

    p1.update(env)
    p2.update(env)

    if show_board:
        env.print_board()

print('Generating initial value functions...')

possible_states = generate_possible_states( Enviroment() )

value_function_1 = generate_value_function(possible_states, 1)
value_function_2 = generate_value_function(possible_states, 2)

p1 = Agent(p=1, epsilon=0.1, learn_rate=0.5, value_function=value_function_1, verbose=False)
p2 = Agent(p=2, epsilon=0.1, learn_rate=0.5, value_function=value_function_2, verbose=False)
num_of_episodes = 10000

print('Training for', num_of_episodes, 'episodes...')

for i in range(num_of_episodes):
    play_game( p1, p2, Enviroment() )

p1.set_verbose(True)
p1.set_epsilon(0)
p2 = Human(2)

while True:
	play_game(p1, p2, Enviroment(), show_board=True)

	answer = input('\nPlay again? (y): ')
	if answer.lower()[0] != 'y':
		break
