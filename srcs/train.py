import argparse
from srcs.agent import Agent
from srcs.deep_q_network import DQNAgent


def main():
    parser = argparse.ArgumentParser(
        description="Train a Snake RL agent (tabular Q-learning or DQN)"
    )
    parser.add_argument(
        "-e",
        "--episodes",
        type=int,
        default=100,
        help="Number of training episodes (default: 100)",
    )
    parser.add_argument(
        "--show-render",
        action="store_true",
        help="Show a graph of the training progress (scores per episode) after training",
    )
    parser.add_argument(
        "-d",
        "--display",
        action="store_true",
        help="Display the grid during training",
    )
    parser.add_argument(
        "-save",
        type=str,
        default=None,
        metavar="PATH",
        help="Path to save the trained model (Q-table .pkl or DQN .pth)",
    )
    parser.add_argument(
        "-load",
        type=str,
        default=None,
        metavar="PATH",
        help="Path to load a pre-trained model (Q-table .pkl or DQN .pth)",
    )
    parser.add_argument(
        "-dontlearn",
        action="store_true",
        help="Do not train the agent",
    )
    parser.add_argument(
        "--grid",
        type=int,
        default=None,
        metavar="N",
        help="Board size in cells (default: from constants.py)",
    )
    parser.add_argument(
        "-dqn",
        action="store_true",
        help="Use Deep Q-Network for training",
    )
    args = parser.parse_args()

    if args.dqn:
        agent = DQNAgent()
    else:
        agent = Agent(grid_size=args.grid)

    agent.preconfigure(args.load, args.dontlearn)
    agent.train(
        episodes=args.episodes,
        display=args.display,
        learn=not args.dontlearn,
    )
    agent.postconfigure(args.episodes, args.save, args.show_render)


if __name__ == "__main__":
    main()
