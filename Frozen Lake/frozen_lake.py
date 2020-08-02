import frozen_lake_monte_carlo
import frozen_lake_q_learning
import frozen_lake_q_lambda_learning
import matplotlib.pyplot as plt

mc_steps = frozen_lake_monte_carlo.train(epsilon=0.1, gamma=0.5)
q_steps = frozen_lake_q_learning.train(epsilon=0.1, gamma=0.3, alpha=0.7)
q_lambda_steps = frozen_lake_q_lambda_learning.train(epsilon=0.1, gamma=0.3, alpha=0.7, lambda_=0.75)

plt.plot(mc_steps, color='green')
plt.plot(q_steps, color='blue')
plt.plot(q_lambda_steps, color='red')
plt.xlabel('#Episode')
plt.ylabel('Steps')
plt.legend( ('Monte-Carlo',
            'Q-Learning',
            'Q-Lambda-Learning'),
            loc='upper left')
plt.show()