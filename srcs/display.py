import os
import numpy as np
import matplotlib.pyplot as plt


def moving_average(scores: list, window=10) -> np.ndarray:
    if len(scores) < window:
        return np.array([])
    weights = np.ones(window) / window
    return np.convolve(scores, weights, mode="valid")


def plot_scores(scores: list, window=10) -> None:
    if not scores:
        return

    episodes = np.arange(1, len(scores) + 1)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(
        episodes,
        scores,
        color="#a8a8ff",
        alpha=0.4,
        linewidth=0.5,
        label="Raw Scores",
    )

    ma = moving_average(scores, window)
    if len(ma) > 0:
        ma_episodes = np.arange(window, len(scores) + 1)
        ax.plot(
            ma_episodes,
            ma,
            color="red",
            linewidth=2,
            label=f"Moving Average ({window} episodes)",
        )

    ax.set_xlabel("Episode")
    ax.set_ylabel("Score")
    ax.set_title("Training Progress")
    ax.legend(loc="upper left")
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    save_path = os.path.join("graphs", "training_progress.png")
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=120)
    plt.close()
    print(f"Training plot saved to {save_path}")
