import random
import numpy as np
import matplotlib.pyplot as plt


class SnakeAI:

    def __init__(self):
        self.n_actions = 4
        self.q_table = {}
        self.learning_rate = 0.8
        self.discount_factor = 0.95
        self.epsilon = 0.2

    def add_state(self, state):
        if state not in self.q_table:
            self.q_table[state] = np.zeros(self.n_actions)

    def update_q_table(self, state, action, reward, next_state):
        self.add_state(next_state)
        # Implement Bellman equation to calculate the expected future reward
        self.q_table[state][action] += self.learning_rate * (
            reward
            + self.discount_factor * np.max(self.q_table[next_state])
            - self.q_table[state][action]
        )

    def epsilon_greedy_policy(self, state):
        random_int = random.uniform(0, 1)
        if random_int > self.epsilon:
            action = np.argmax(self.q_table[state])
        else:
            action = random.randint(0, self.n_actions - 1)
        return action

    def choose_action(self, state):
        self.add_state(state)
        return self.epsilon_greedy_policy(state)
