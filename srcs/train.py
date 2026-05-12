import argparse
from srcs.snakeAI import SnakeAI


def main():
    parser = argparse.ArgumentParser(description="Train the Snake Q-learning agent")
    parser.add_argument(
        "-e",
        "--episodes",
        type=int,
        default=100,
        help="Number of training episodes (default: 100)",
    )
    parser.add_argument(
        "--display",
        action="store_true",
        help="Display the board during training",
    )
    parser.add_argument(
        "-save",
        type=str,
        default=None,
        metavar="PATH",
        help="Path to save the trained Q-table (e.g. models/10sess.txt)",
    )
    parser.add_argument(
        "-load",
        type=str,
        default=None,
        metavar="PATH",
        help="Path to load the pre-trained Q-table (e.g. models/10sess.txt)",
    )
    parser.add_argument(
        "-dontlearn",
        action="store_true",
        help="Do not train the agent",
    )
    args = parser.parse_args()
    agent = SnakeAI()

    if args.load:
        agent.load_q_table(args.load)
        agent.max_epsilon = 0

    agent.train(episodes=args.episodes, display=args.display, learn=not args.dontlearn)
    if args.save:
        agent.save_q_table(args.save)
        print(f"Q-table saved to {args.save}")


if __name__ == "__main__":
    main()
