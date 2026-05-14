# 🐍 learn2slither_42

## Introduction

The goal of this project is to teach a snake to play by itself using **Reinforcement Learning** — without any hardcoded strategy. The agent learns purely from trial and error: it tries actions, observes rewards, and gradually figures out a winning policy.

Two algorithms are implemented:

- **Tabular Q-Learning** — the classic approach using a lookup table
- **Deep Q-Network (DQN)** — a neural network approximation using PyTorch

---

## Game rules

By default, the board is a 10×10 grid (8×8 playable area + walls). The snake starts with 3 segments at a random position and direction.

| Element | Effect |
|---------|--------|
| 🟢 Green apple (×2) | Snake grows by 1 cell |
| 🔴 Red apple (×1) | Snake shrinks by 1 cell |
| Wall / self collision | Game over |
| Shrink to 0 cells | Game over |

The snake chooses one of 4 actions: `UP`, `DOWN`, `LEFT`, `RIGHT`. The snake cannot make a 180° U-turn.

---

## Q-Learning

Q-Learning teaches the agent which action `a` is best in each state `s`. It maintains a function `Q(s, a)` that estimates the **expected total future reward** of taking action `a` in state `s`.

The agent learns by repeatedly applying the **Bellman equation** to update its estimates:

```
Q(s, a) ← Q(s, a) + α · [ r + γ · max(Q(s', a')) − Q(s, a) ]
```

Where:

- `α` (`learning_rate`) — how much new information overrides old
- `γ` (`discount_rate`) — how much we value future rewards
- `r` — immediate reward
- `s'` — next state
- `max(Q(s', a'))` — best estimated future value

### ε-greedy policy

To balance **exploration** (trying new things) and **exploitation** (using what works), the agent uses an **ε-greedy** strategy:

- With probability `ε` → pick a **random** action (explore)
- With probability `1 − ε` → pick the **best known** action (exploit)

`ε` starts high (~1.0, full exploration) and decays toward a minimum (~0.01) so the agent gradually trusts its own knowledge.

---

## State representation

Each state is encoded as a **12-bit binary tuple** capturing what the snake needs to know:

| Bits | Feature | Encoding |
|------|---------|----------|
| 0–3 | Current direction | one-hot: UP / RIGHT / DOWN / LEFT |
| 4–7 | Closest green apple direction | up / right / down / left |
| 8–11 | Immediate danger | wall / body / red apple in each cardinal direction |

This compact encoding bounds the state space to **2¹² = 4096 states**, making tabular Q-learning tractable.

---

## Reward function

| Event | Reward |
|-------|--------|
| Eat green apple | **+10** |
| Eat red apple | **−10** |
| Die (wall / body / shrink to 0) | **−100** |
| Survive one tick | **−1** |

The tick penalty pushes the agent to **finish quickly** instead of looping safely without eating.

---

## Setup

1. Clone the repository

```bash
git clone https://github.com/MatLBS/learn2slither_42.git
cd learn2slither_42
```

2. Install dependencies with [uv](https://github.com/astral-sh/uv)

```bash
uv sync
```

---

## Commands

### Play yourself

```bash
uv run snake                    # default board size
uv run snake --grid 10          # custom board size
uv run snake -sbs               # step-by-step mode
```

Press `TAB` during play to cycle through speeds (×0.5, ×1, ×2, ×5).

### Train a tabular agent (1000 episodes)

```bash
uv run train -e 1000 -save models/1000ep.pkl --show-render
```

### Watch the trained tabular agent play

```bash
uv run train -e 100 -load models/1000ep.pkl -d -dontlearn
```

### Train with Deep Q-Network (1000 episodes)

```bash
uv run train -e 1000 -dqn -save models/1000ep.pth --show-render
```

### Watch the trained DQN agent play

```bash
uv run train -e 100 -dqn -load models/1000ep.pth -d -dontlearn
```

---

## Deep Q-Network

A neural network approximates `Q(s, a)` instead of a lookup table:

- Architecture: `12 → 128 → 128 → 4` (ReLU activations)
- Experience replay buffer (10,000 transitions)
- Target network synchronized every 1000 optimization steps
- Optimizer: Adam (`lr = 1e-3`)
- Mini-batch size: 64

For a small state space like ours (12 binary features), **the tabular agent actually performs better** — DQN's function approximation introduces noise that the tabular version doesn't suffer from. DQN shines when the state space becomes too large to enumerate.

---

## CLI options

### `uv run train`

| Option | Description |
|--------|-------------|
| `-e N`, `--episodes N` | Number of training episodes (default: 100) |
| `-d`, `--display` | Render the board during training |
| `--show-render` | Save the training score graph after training |
| `-save PATH` | Save the trained model |
| `-load PATH` | Load a pre-trained model |
| `-dontlearn` | Play without updating the model (eval mode) |
| `--grid N` | Board size in cells |
| `-dqn` | Use Deep Q-Network instead of tabular Q-learning |

### `uv run snake`

| Option | Description |
|--------|-------------|
| `-sbs` | Step-by-step: snake advances only on arrow press |
| `--grid N` | Board size in cells |

In-game key bindings:

| Key | Action |
|-----|--------|
| Arrow keys | Move snake |
| `TAB` | Cycle display speed |
| `SPACE` | Restart after game over |

---

## Project structure

```
learn2slither_42/
├── srcs/
│   ├── main.py             # Human play entry point
│   ├── train.py            # Training entry point (CLI)
│   ├── environment.py      # Game env (state, step, reward, render)
│   ├── snake.py            # Snake class (move, grow, shrink)
│   ├── apple.py            # Green & red apples
│   ├── constants.py        # Screen size, colors, FPS, speeds
│   ├── agent.py            # Tabular Q-Learning agent
│   ├── deep_q_network.py   # DQN agent (PyTorch)
│   └── display.py          # Score plot (matplotlib)
├── models/                 # Saved models (.pkl tabular / .pth DQN)
├── graphs/                 # Training progress plots
└── pyproject.toml          # uv project config
```
