import sys
import pygame
from srcs.constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    CELL_SIZE,
    GRID_SIZE,
    FPS,
    BACKGROUND_COLOR,
    BORDER_COLOR,
    SCORE_COLOR,
    UP,
    DOWN,
    LEFT,
    RIGHT,
)
from srcs.snake import Snake
from srcs.apple import Apple, RedApple


class Environment:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.reset()

    def reset(self) -> None:
        self.snake = Snake()
        self.green_apples = []
        self.red_apple = RedApple(list(self.snake.positions))
        for _ in range(2):
            forbidden = (
                list(self.snake.positions)
                + [self.red_apple.position]
                + [a.position for a in self.green_apples]
            )
            self.green_apples.append(Apple(forbidden))
        self.score = 0

    def get_state(self) -> str:
        head_x, head_y = self.snake.positions[0]
        body = set(self.snake.positions[1:])
        green_positions = {a.position for a in self.green_apples}
        red_position = self.red_apple.position

        def cell_char(x: int, y: int) -> str:
            if x == 0 or x == GRID_SIZE - 1 or y == 0 or y == GRID_SIZE - 1:
                return "W"
            if (x, y) == (head_x, head_y):
                return "H"
            if (x, y) in body:
                return "S"
            if (x, y) in green_positions:
                return "G"
            if (x, y) == red_position:
                return "R"
            return "0"

        row = "".join(cell_char(x, head_y) for x in range(GRID_SIZE))
        col = "".join(cell_char(head_x, y) for y in range(GRID_SIZE))
        return row + "_" + col

    def render(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        self._draw()
        pygame.display.flip()
        self.clock.tick(FPS)

    def determine_reward(self, done: bool, event: str | None) -> int:
        if not done:
            return -100
        elif event == "red":
            return -10
        elif event == "green":
            return 10
        else:
            return -1

    def step(self, action: tuple[int, int]) -> tuple:
        if action == UP:
            self.snake.change_direction((0, -1))
        elif action == DOWN:
            self.snake.change_direction((0, 1))
        elif action == LEFT:
            self.snake.change_direction((-1, 0))
        elif action == RIGHT:
            self.snake.change_direction((1, 0))
        done, event = self._update()
        reward = self.determine_reward(done, event)
        new_state = self.get_state() if done else None
        return (new_state, reward, done)

    def _all_apples(self) -> list:
        return [self.red_apple] + self.green_apples

    def _obstacles_excluding(self, apple: Apple) -> list:
        positions = list(self.snake.positions)
        for other in self._all_apples():
            if other is apple:
                continue
            positions.append(other.position)
        return positions

    def run(self) -> None:
        while True:
            self._handle_events()
            done, _ = self._update()
            self._draw()
            pygame.display.flip()
            self.clock.tick(FPS)

            if not done:
                self._show_end_screen("GAME OVER")
            elif len(self.snake.positions) == GRID_SIZE * GRID_SIZE:
                self._show_end_screen("YOU WIN!")

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake.change_direction((0, -1))
                elif event.key == pygame.K_DOWN:
                    self.snake.change_direction((0, 1))
                elif event.key == pygame.K_LEFT:
                    self.snake.change_direction((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    self.snake.change_direction((1, 0))

    def _update(self) -> tuple[bool, str | None]:
        if not self.snake.move():
            return False, None
        head = self.snake.positions[0]
        for apple in self._all_apples():
            if head == apple.position:
                point = apple.on_eat(self.snake)
                self.score += point
                if not self.snake.positions:
                    return False, None
                apple.respawn(self._obstacles_excluding(apple))
                if point == 0:
                    return True, "red"
                else:
                    return True, "green"
        return True, None

    def _draw(self) -> None:
        self.screen.fill(BACKGROUND_COLOR)
        pygame.draw.rect(
            self.screen,
            BORDER_COLOR,
            pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT),
            CELL_SIZE,
        )
        self.snake.draw(self.screen)
        for apple in self._all_apples():
            apple.draw(self.screen)
        score_text = self.font.render(f"Score: {self.score}", True, SCORE_COLOR)
        self.screen.blit(score_text, (10, 10))

    def _show_end_screen(self, title: str) -> None:
        self.screen.fill(BACKGROUND_COLOR)
        title_surf = self.font.render(title, True, SCORE_COLOR)
        score_surf = self.font.render(f"Score: {self.score}", True, SCORE_COLOR)
        restart_surf = self.font.render("Press Space to Restart", True, SCORE_COLOR)
        cx = SCREEN_WIDTH // 2
        self.screen.blit(
            title_surf, (cx - title_surf.get_width() // 2, SCREEN_HEIGHT // 4)
        )
        self.screen.blit(
            score_surf, (cx - score_surf.get_width() // 2, SCREEN_HEIGHT // 3)
        )
        self.screen.blit(
            restart_surf,
            (cx - restart_surf.get_width() // 2, SCREEN_HEIGHT // 2),
        )
        pygame.display.flip()
        self._wait_for_restart()

    def _wait_for_restart(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.reset()
                    return
