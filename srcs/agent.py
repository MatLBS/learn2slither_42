import os
import random
import numpy as np
from tqdm import tqdm
from srcs.environment import Environment


class Agent:
    def __init__(self):
        self.n_actions = 4
        self.q_table = {}
        self.learning_rate = 0.1
        self.discount_rate = 0.95
        self.max_epsilon = 1.0
        self.min_epsilon = 0.05
        self.decay_rate = 0.00005
        self.env = Environment()

    def add_state(self, state: str) -> None:
        if state not in self.q_table:
            self.q_table[state] = np.zeros(self.n_actions)

    def update_q_table(
        self, state: str, action: int, reward: int, new_state: str | None
    ) -> None:
        if new_state is None:
            future_value = 0.0
        else:
            self.add_state(new_state)
            future_value = np.max(self.q_table[new_state])
        self.q_table[state][action] += self.learning_rate * (
            reward + self.discount_rate * future_value - self.q_table[state][action]
        )

    def epsilon_greedy_policy(self, state: str) -> int:
        random_int = random.uniform(0, 1)
        if random_int > self.max_epsilon:
            action = np.argmax(self.q_table[state])
        else:
            action = random.randint(0, self.n_actions - 1)
        self.max_epsilon = max(self.min_epsilon, self.max_epsilon - self.decay_rate)
        return action

    def choose_action(self, state: str) -> int:
        self.add_state(state)
        return self.epsilon_greedy_policy(state)

    def save_q_table(self, path: str) -> None:
        directory = os.path.dirname(path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        with open(path, "w") as f:
            for state, values in self.q_table.items():
                line = state + " " + " ".join(str(v) for v in values)
                f.write(line + "\n")

    def load_q_table(self, path: str) -> None:
        with open(path, "r") as f:
            for line in f:
                parts = line.strip().split()
                state = parts[0]
                values = np.array([float(x) for x in parts[1:]])
                self.q_table[state] = values

    def train(self, episodes=100, display=False, learn=True) -> list[int]:
        scores = []
        for episode in tqdm(range(episodes), desc="Training", unit="ep"):
            self.env.reset()
            state = self.env.get_state()
            episode_score = 0

            while True:
                action = self.choose_action(state)
                new_state, reward, done = self.env.step(action)
                if learn:
                    self.update_q_table(state, action, reward, new_state)
                episode_score += reward
                if not done:
                    break
                state = new_state
                if display:
                    self.env.render()
            scores.append(episode_score)
        return scores
