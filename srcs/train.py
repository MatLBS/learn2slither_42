from srcs.game import Game
from srcs.snakeAI import SnakeAI


def train(sessions=100, display=False):
    agent = SnakeAI()
    game = Game()

    for episode in range(sessions):
        state = game.get_state()
        while True:
            action = agent.choose_action(state)
            next_state, reward, alive = game.step(action)
            agent.update_q_table(state, action, reward, next_state)
            state = next_state
            if display:
                game.render()
            if not alive:
                break
        game._reset()


def main():
    train(display=True)


if __name__ == "__main__":
    main()
