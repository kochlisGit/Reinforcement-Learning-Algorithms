import math
import random as rand
import matplotlib.pyplot as plt

def sample(mean, lamda):
		return rand.random() / math.sqrt(lamda) + mean

class Bandit:
    def __init__(self, win_prob):
        self.win_prob = win_prob
        self.mean = 0
        self.sum_x = 0
        self.N = 0
        self.lamda = 1
        self.t = 1

    def pull(self):
        p = rand.randint(1, 100)
        if p < self.win_prob:
            return 1
        else:
            return -1

    def update(self, x):
        self.sum_x += x
        self.lamda += self.t
        self.mean = self.t*self.sum_x / self.lamda
        self.N += 1

    def __str__(self):
        return 'Win Prob = ' + str(self.win_prob) + '%' + \
        ', Mean = ' + str(self.mean) + \
        ', Num of games played = ' + str(self.N)

def play(N):
    bandits = [ Bandit(20), Bandit(40), Bandit(60) ]
    profit = 0
    profit_timeline = [profit]

    for i in range(N):
        samples = [sample(band.mean, band.lamda) for band in bandits]
        b = samples.index( max(samples) )
        x = bandits[b].pull()
        bandits[b].update(x)

        profit += x
        profit_timeline.append(profit)

    print('\nBayesian Sampling')
    for b in bandits:
        print(b)

    return profit_timeline

def plot_experiment():
    profit_timeline = play(N=1000)

    plt.plot([ i for i in range( len(profit_timeline) ) ], profit_timeline, color='pink')
    plt.title('Epsilon Greedy in 1000 games')
    plt.xlabel('Time')
    plt.ylabel('Profit')