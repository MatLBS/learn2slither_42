import sys
import pygame
from srcs.constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    GRID_SIZE,
    FPS,
    SPEEDS,
    DEFAULT_SPEED_IDX,
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
    def __init__(self, grid_size: int = GRID_SIZE):
        self.grid_size = grid_size
        self.cell_size = SCREEN_WIDTH // grid_size
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.speed_idx = DEFAULT_SPEED_IDX
        self.step_by_step = False
        self.reset()

    def reset(self) -> None:
        self.snake = Snake(self.grid_size, self.cell_size)
        self.green_apples = []
        self.red_apple = RedApple(
            list(self.snake.positions), self.grid_size, self.cell_size
        )
        for _ in range(2):
            forbidden = (
                list(self.snake.positions)
                + [self.red_apple.position]
                + [a.position for a in self.green_apples]
            )
            self.green_apples.append(Apple(forbidden, self.grid_size, self.cell_size))
        self.score = 0

    def get_state(self) -> str | None:
        if not self.snake.positions:
            return None

        head_x, head_y = self.snake.positions[0]
        body = set(self.snake.positions[1:])
        red_position = self.red_apple.position
        state = []

        def is_danger(x: int, y: int) -> int:
            if x <= 0 or x >= self.grid_size - 1:
                return 1
            if y <= 0 or y >= self.grid_size - 1:
                return 1
            if (x, y) in body:
                return 1
            if (x, y) == red_position:
                return 1
            return 0

        dx, dy = self.snake.direction
        dir_u = (dx, dy) == (0, -1)
        dir_r = (dx, dy) == (1, 0)
        dir_d = (dx, dy) == (0, 1)
        dir_l = (dx, dy) == (-1, 0)

        food = min(
            self.green_apples,
            key=lambda a: abs(a.position[0] - head_x) + abs(a.position[1] - head_y),
        )
        food_x, food_y = food.position

        state.append(int(dir_u))
        state.append(int(dir_r))
        state.append(int(dir_d))
        state.append(int(dir_l))
        state.append(int(food_y < head_y))
        state.append(int(food_x > head_x))
        state.append(int(food_y > head_y))
        state.append(int(food_x < head_x))
        state.append(is_danger(head_x, head_y - 1))
        state.append(is_danger(head_x + 1, head_y))
        state.append(is_danger(head_x, head_y + 1))
        state.append(is_danger(head_x - 1, head_y))
        return tuple(state)

    def _cycle_speed(self) -> None:
        self.speed_idx = (self.speed_idx + 1) % len(SPEEDS)

    def render(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                self._cycle_speed()
        self._draw()
        pygame.display.flip()
        self.clock.tick(FPS * SPEEDS[self.speed_idx])

    def determine_reward(self, done: bool, event: str | None) -> int:
        if done:
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
        next_state = self.get_state() if not done else None
        return (next_state, reward, done)

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
            arrow_pressed = self._handle_events()
            if not self.step_by_step or arrow_pressed:
                done, _ = self._update()
            else:
                done = False
            self._draw()
            pygame.display.flip()
            self.clock.tick(FPS * SPEEDS[self.speed_idx])

            if done:
                self._show_end_screen("GAME OVER")
            elif len(self.snake.positions) == self.grid_size * self.grid_size:
                self._show_end_screen("YOU WIN!")

    def _handle_events(self) -> bool:
        arrow_pressed = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    self._cycle_speed()
                elif event.key == pygame.K_UP:
                    self.snake.change_direction((0, -1))
                    arrow_pressed = True
                elif event.key == pygame.K_DOWN:
                    self.snake.change_direction((0, 1))
                    arrow_pressed = True
                elif event.key == pygame.K_LEFT:
                    self.snake.change_direction((-1, 0))
                    arrow_pressed = True
                elif event.key == pygame.K_RIGHT:
                    self.snake.change_direction((1, 0))
                    arrow_pressed = True
        return arrow_pressed

    def _update(self) -> tuple[bool, str | None]:
        if not self.snake.move():
            return True, None
        head = self.snake.positions[0]
        for apple in self._all_apples():
            if head == apple.position:
                point = apple.on_eat(self.snake)
                self.score += point
                if not self.snake.positions:
                    return True, None
                apple.respawn(self._obstacles_excluding(apple))
                if point == 0:
                    return False, "red"
                else:
                    return False, "green"
        return False, None

    def _draw(self) -> None:
        self.screen.fill(BACKGROUND_COLOR)
        pygame.draw.rect(
            self.screen,
            BORDER_COLOR,
            pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT),
            self.cell_size,
        )
        self.snake.draw(self.screen)
        for apple in self._all_apples():
            apple.draw(self.screen)
        score_text = self.font.render(f"Score: {self.score}", True, SCORE_COLOR)
        self.screen.blit(score_text, (10, 10))
        speed_text = self.font.render(
            f"Speed: x{SPEEDS[self.speed_idx]}", True, SCORE_COLOR
        )
        self.screen.blit(speed_text, (10 + score_text.get_width() + 20, 10))

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
