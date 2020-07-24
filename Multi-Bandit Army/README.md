# Multi-Bandit Army Problem

Suppose You are at a casino and You have the option of playing 3 different machines. Each machine has its own winning probability. Every time You play a machine, You either win a coin or lose one. Your goal is to get as many coins as possible by playing the machines. 

The winning probabilities are stationary, meaning that they don't change over the time. However, You don't know the exact winning probability of each machine, so You have play it (explore it) a couple of times to learn it. After You find the machine with the largest winning probability, then You stop exploring and play only that particular machine (Exploitation). I've tried and compared the following algorithms:

1. Epsilon Greedy (e = 0.05)

1. Epsilon Greedy Modified (e = 1/n), where n --> the n-th game.

1. Optimistic Initial Values (X_0 = 10)

1. UCB

1. Thompson Sampling (l = 1, t = 1)

# Results

I have run each algorithm for N = 1000 games. The results are shown in the graphs below:


![Run1](https://github.com/kochlisGit/Reinforcement-Learning/blob/master/Multi-Bandit%20Army/vis_1.png)

![Run2](https://github.com/kochlisGit/Reinforcement-Learning/blob/master/Multi-Bandit%20Army/vis_2.png)

![Run3](https://github.com/kochlisGit/Reinforcement-Learning/blob/master/Multi-Bandit%20Army/vis_3.png)

![Run4](https://github.com/kochlisGit/Reinforcement-Learning/blob/master/Multi-Bandit%20Army/vis_4.png)

![Run5](https://github.com/kochlisGit/Reinforcement-Learning/blob/master/Multi-Bandit%20Army/vis_5.png)

Epsilon Greedy with a constant is the most used algorithm today, because of its simplicity. However, we notice that _Bayesian Sampling_ and _Optimistic Initial Values method_ outperform every other algorithm almost every time.

You can run the file and test the results by yourself:

**python -m multi_bandit_army.py**

# Important Note about Multi-Army Bandit

You might wonder how You can use Multi-Army Bandit solutions to a Casino. Thething is, **You can't**. The reason why these algorithms work and do produce some profit is because the 3 machines in the example have:

1. 20% Winrate

1. 40% Winrate

1. 60% Winrate

The algorithms try to find the machine with the 60% winning probability and then start to exloit. But why those algorithms won't work in a casino?

Casino's machine have about 20-25% winning probability. It means that If you play 4-5 times, You will probably win 1 or 2 times at most, but lose the rest of the times.
If You have infinite money and keep playing forever, according to the Central Limit Theorem, It is proven that You will lose a lot of coins. So, even If You waste a lot of money to find the machine that has the most winning chances, You won't be able to exploit it.
