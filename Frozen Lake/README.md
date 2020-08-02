# Frozen Lake - Description

I've made a simple game, in order to test 3 important algorithms: 

1. Monte-Carlo

1. Q Learning

1. Q(lambda) Learning

In this game, an agent begins at the starting position on a frozen lake. The agent can move freely on the lake (UP, DOWN, LEFT, RIGHT). The goal is to reach one of the terminal states (Goals). 
In order to make it harder, I have added some holes on the lake. If the agent falls on a hole, he loses the game.

The agent deploys an Exploration-Exploitation strategy in order to learn as fast as possible. The agent uses the modified epsilon greedy strategy in order to take an action at each step of the game.

# Modified Epsilon Greedy

In each step, the agent picks a random number p between (0.0, 1.0).

    If p < epsilon, then the agent chooses a random action:
      action = random( Q[state] )
    else:
      action = Q'[state]
      
The epsilon is a constant set to 0.1 by default. However, if the modified epsilon greedy is used, then epsilon is a parameter, which starts with a high value of 1.0, so that the agent explores the enviroment enough times to find the best path. In every episode, the epsilon is reduced exponentially:

    (e = 1/i)
    
where i is the i-th episode.
      
Q[s] is the Q Function of the 4 states: Q[state][UP], Q[state][DOWN], Q[state][LEFT], Q[state][RIGHT]
and Q[state'] is the highest value of the current state's actions.
 
# Quality Function
 
The Q (Quality) Function is a value function, which is used by the agent, in order to decide what's the best action to make. 
 
So, the Q function is an array of shape (num_of_states, num_of_actions). 
 
Note: In monte-carlo updates, I've used a simple value function, instead of Q, which is an array of (num_of_states) cells, because in monte-carlo we are not interested in the remembering the best actions.
 
# Comparisons & Results

As you can see in plots above, all algorithms are pretty solid and converge within the first 10-20 episodes.

![Run1](https://github.com/kochlisGit/Reinforcement-Learning/blob/master/Frozen%20Lake/vis_1.png)

![Run2](https://github.com/kochlisGit/Reinforcement-Learning/blob/master/Frozen%20Lake/vis_2.png)

![Run3](https://github.com/kochlisGit/Reinforcement-Learning/blob/master/Frozen%20Lake/vis_3.png)

![Run4](https://github.com/kochlisGit/Reinforcement-Learning/blob/master/Frozen%20Lake/vis_4.png)

![Run5](https://github.com/kochlisGit/Reinforcement-Learning/blob/master/Frozen%20Lake/vis_5.png)
 
