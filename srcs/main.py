import argparse
from srcs.environment import Environment


def main():
    parser = argparse.ArgumentParser(description="Play Snake")
    parser.add_argument(
        "-sbs",
        action="store_true",
        help="Step-by-step mode: snake advances one cell per arrow press",
    )
    parser.add_argument(
        "--board",
        type=int,
        default=None,
        metavar="N",
        help="Board size in cells (default: from constants.py)",
    )
    args = parser.parse_args()

    if args.board is not None:
        env = Environment(grid_size=args.board)
    else:
        env = Environment()
    env.step_by_step = args.sbs
    env.run()


if __name__ == "__main__":
    main()
