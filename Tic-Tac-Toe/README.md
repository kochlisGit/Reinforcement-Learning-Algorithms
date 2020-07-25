# Tic Tac Toe with Reinforcement Learning

In this project, I created an agent that learns how to play tic-tac-toe by playing against himself. Tic-Tac-Toe is an 1v1 game played on a 3x3 board. Each player gets a letter
('O' / 'X'). Initially, all squares on the board are empty. Each player puts a letter on the board one after another. The player that first puts 3 letters in a row or a column
or a diagonal, wins. The player with the letter 'O' starts first.

For example, such a screenshot of the game could be the following:

O | X | O
----------
O | O | X
----------
X | X | O

In this example, The player with the letter 'O' wins the game, because he managed to put 3 Os in a diagonal.

# Naive Approach

One Naive approach would be to construct rules so that the agent never loses. For example, such rules could be:

1. If You start first, always place your letter in the center.

1. If the other player puts 2 of his letters in a row, then put yours on the third place.

etc

# Rewards & Value Function

The agent will play against himself many times and remember every state of the game and the result of the game. At the end of the game, the enviroment will reward the agent
If he won the game or give him a penalty if he loses. To do that, we need to contruct a value function that tells the agent every time, what's the state with the higher reward
(higher probability to win the game).

So, i came up with a value function is a list of 19683 states (3^9). Initially, each state has the following values:

* 1 If it is a winning state (such as in the above example).

* 0 If it is a losing state.

* 0.5 Otherwise.

The agent then will play vs another agent with the opposite letter and try to beat him every time, using the epsilon greedy algorithm (with e = 0.1).
At the end of the game, the agent updates the values of each state of the game in the value function and plays again.

I found that 10000 episodes are more than enough for the agent to reach the 'god mode', in which he never loses.

# Running the game

Enter the following command in your terminal: ** python -m tic_tac_toe.py **

Wait for the agent to train himself. This takes less than 5 seconds. Then You can test the agent by yourself. By default, i choosed the agent to play always first.
I did this, because I wanted to test the agent If he always puts 'O' in the middle, first. This is proven to have the highest winning chances.
