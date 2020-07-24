import epsilon_greedy
import epsilon_greedy_modified
import initial_optimistic_values
import UCB1
import bayesian_sampling
import matplotlib.pyplot as plt

N = 1000

eps_greedy_prof = epsilon_greedy.play(N, epsilon=0.05)
eps_greedy_mod_prof = epsilon_greedy_modified.play(N)
init_opt_val = initial_optimistic_values.play(N)
ucb_prof = UCB1.play(N)
bayes_samlping_prof = bayesian_sampling.play(N)

x = [ i for i in range(N+1) ]
plt.plot(x, eps_greedy_prof, color = 'blue')
plt.plot(x, eps_greedy_mod_prof, color = 'cyan')
plt.plot(x, init_opt_val, color = 'green')
plt.plot(x, ucb_prof, color = 'red')
plt.plot(x, bayes_samlping_prof, color = 'pink')

plt.xlabel('Time')
plt.ylabel('Profit')
plt.title('Exploration-Exploitation Algorithms')
plt.legend( ('Epsilon Greedy',
            'Modified Epsilon Greedy',
            'Initial Optimistic Values',
            'UCB',
            'Bayesian Sampling'),
            loc='upper left')

plt.show()