import os
import random
import numpy as np
from tqdm import tqdm
import pickle
from srcs.environment import Environment
from srcs.display import plot_scores


class Agent:
    def __init__(self, grid_size: int | None = None):
        self.n_actions = 4
        self.q_table = {}
        self.lr = 0.1
        self.discount_rate = 0.95
        self.epsilon_max = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.scores = []
        if grid_size is None:
            self.env = Environment()
        else:
            self.env = Environment(grid_size=grid_size)

    def add_state(self, state: str) -> None:
        if state not in self.q_table:
            self.q_table[state] = np.zeros(self.n_actions)

    def update_q_table(
        self, state: str, action: int, reward: int, next_state: str | None
    ) -> None:
        if next_state is None:
            future_value = 0.0
        else:
            self.add_state(next_state)
            future_value = np.max(self.q_table[next_state])
        self.q_table[state][action] += self.lr * (
            reward + self.discount_rate * future_value - self.q_table[state][action]
        )

    def epsilon_greedy_policy(self, state: str) -> int:
        random_int = random.uniform(0, 1)
        if random_int > self.epsilon_max:
            action = np.argmax(self.q_table[state])
        else:
            action = random.randint(0, self.n_actions - 1)
        return action

    def choose_action(self, state: str) -> int:
        self.add_state(state)
        return self.epsilon_greedy_policy(state)

    def save_q(self, path: str) -> None:
        directory = os.path.dirname(path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        with open(path, "wb") as f:
            pickle.dump(self.q_table, f)
        print(f"Q-table saved to {path}")

    def load_q(self, path: str) -> None:
        with open(path, "rb") as f:
            self.q_table = pickle.load(f)

    def preconfigure(self, load=None, dontlearn=False) -> None:
        if load:
            self.load_q(load)
        if dontlearn:
            self.epsilon_max = 0

    def postconfigure(self, episodes, save=None, show_render=False) -> None:
        if save:
            self.save_q(save)
        if show_render:
            plot_scores(self.scores, episodes, window=100)

    def train(self, episodes=100, display=False, learn=True) -> list[int]:
        for episode in tqdm(range(episodes), desc="Training", unit="ep"):
            self.env.reset()
            state = self.env.get_state()
            episode_score = 0

            while True:
                action = self.choose_action(state)
                next_state, reward, done = self.env.step(action)
                if learn:
                    self.update_q_table(state, action, reward, next_state)
                episode_score += reward
                if done:
                    break
                state = next_state
                if display:
                    self.env.render()

            self.scores.append(episode_score)
            self.epsilon_max = max(
                self.epsilon_min, self.epsilon_decay * self.epsilon_max
            )
