# Reinforcement-Learning-Algorithms
This project focuses on comparing different Reinforcement Learning Algorithms. I have implemented 3 custom **(Openai-Gym like)** environments to test my algorithms:

1. Tic-Tac-Toe (The classical tic-tac-toe game)
1. Frozen Lake (Custom implementation of the openai-gym frozen lake)
1. Multi-Bandit-Army (Exploration & Exploitation of the best-winning-chance fruit machine)

#**Exploration - Exploitation Algorithms**

# Epsilon Greedy
The agent explores every possible action with a small probability, but most often exploits the best action: https://www.ijntr.org/download_data/IJNTR06090006.pdf

# Decaying Epsilon Greedy
The agent starts by exploring every possible action with very high initial probability, however, this probability decays over the time. This is an improvement of Epsilon-Greedy
algorithm: http://tokic.com/www/tokicm/publikationen/papers/AdaptiveEpsilonGreedyExploration.pdf

# Initial Optimistic Values
Initially, all actions are considered to be the best. While the agent always exploits the best possible action from a state, the best action will always tend to have the highest
mean reward: https://ieeexplore.ieee.org/document/8167915

# Upper Confidence Bound (UCB)
This tutorial explains very well how this algorithm works and why it is superior to epsilon greedy: https://www.geeksforgeeks.org/upper-confidence-bound-algorithm-in-reinforcement-learning/

# Thompson Sampling (or Bayesian Sampling)
Probably one of the best exploration-exploitation algorithm. However, It is rarely used due to its difficulty in the implementation:
https://proceedings.neurips.cc/paper/2011/file/e53a0a2978c28872a4505bdb51db06dc-Paper.pdf
