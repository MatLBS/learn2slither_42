import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os
import random
from tqdm import tqdm
from collections import deque
from srcs.agent import Agent


class DQN(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(input_dim, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, output_dim)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)

    def save(self, file_name="model.pth"):  # saving the model
        model_folder_path = "./model"
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)


class DQNAgent(Agent):
    def __init__(self):
        super().__init__()
        self.lr = 1e-3
        self.batch_size = 64
        self.target_update_freq = 1000
        self.memory_size = 10000
        self.steps_done = 0

        input_dim = len(self.env.get_state())
        output_dim = self.n_actions
        self.policy_net = DQN(input_dim, output_dim)
        self.target_net = DQN(input_dim, output_dim)
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.target_net.eval()

        self.optimizer = optim.Adam(self.policy_net.parameters(), lr=self.lr)
        self.memory = deque(maxlen=self.memory_size)

    def choose_action(self, state) -> int:
        if random.random() < self.epsilon_max:
            return random.randint(0, self.n_actions - 1)
        with torch.no_grad():
            state_tensor = torch.FloatTensor(state).unsqueeze(0)
            q_values = self.policy_net(state_tensor)
            return int(q_values.argmax(dim=1).item())

    def save_q_table(self, path: str) -> None:
        directory = os.path.dirname(path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        torch.save(self.policy_net.state_dict(), path)
        print(f"Model saved to {path}")

    def load_q_table(self, path: str) -> None:
        state_dict = torch.load(path)
        self.policy_net.load_state_dict(state_dict)
        self.target_net.load_state_dict(state_dict)
        self.target_net.eval()

    def optimize_model(self):
        if len(self.memory) < self.batch_size:
            return

        batch = random.sample(self.memory, self.batch_size)
        state_batch, action_batch, reward_batch, next_state_batch, done_batch = zip(
            *batch
        )

        # Replace None next_states with zero vectors (terminal placeholder)
        state_dim = len(state_batch[0])
        next_state_batch = tuple(
            s if s is not None else (0,) * state_dim for s in next_state_batch
        )

        state_batch = torch.FloatTensor(state_batch)
        action_batch = torch.LongTensor(action_batch).unsqueeze(1)
        reward_batch = torch.FloatTensor(reward_batch)
        next_state_batch = torch.FloatTensor(next_state_batch)
        done_batch = torch.FloatTensor(done_batch)

        # Compute Q-values for current states
        q_values = self.policy_net(state_batch).gather(1, action_batch).squeeze()

        # Compute target Q-values using the target network
        with torch.no_grad():
            max_next_q_values = self.target_net(next_state_batch).max(1)[0]
            target_q_values = reward_batch + self.discount_rate * max_next_q_values * (
                1 - done_batch
            )

        loss = nn.MSELoss()(q_values, target_q_values)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        self.steps_done += 1
        if self.steps_done % self.target_update_freq == 0:
            self.target_net.load_state_dict(self.policy_net.state_dict())

    def train(self, episodes=100, display=False, learn=True) -> list[int]:
        for episode in tqdm(range(episodes), desc="Training", unit="ep"):
            self.env.reset()
            state = self.env.get_state()
            episode_score = 0

            while True:
                action = self.choose_action(state)
                next_state, reward, done = self.env.step(action)

                # Store transition in memory
                self.memory.append((state, action, reward, next_state, done))

                # Optimize model
                if learn:
                    self.optimize_model()

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
