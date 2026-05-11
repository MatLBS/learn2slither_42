import sys
import pygame
from srcs.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE, GRID_SIZE, FPS,
    BACKGROUND_COLOR, BORDER_COLOR, SCORE_COLOR,
)
from srcs.snake import Snake
from srcs.apple import Apple, RedApple


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self._reset()

    def _reset(self):
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

    def _all_apples(self):
        return [self.red_apple] + self.green_apples

    def _obstacles_excluding(self, apple):
        positions = list(self.snake.positions)
        for other in self._all_apples():
            if other is apple:
                continue
            positions.append(other.position)
        return positions

    def run(self):
        while True:
            self._handle_events()
            alive = self._update()
            self._draw()
            pygame.display.flip()
            self.clock.tick(FPS)

            if not alive:
                self._show_end_screen("GAME OVER")
            elif len(self.snake.positions) == GRID_SIZE * GRID_SIZE:
                self._show_end_screen("YOU WIN!")

    def _handle_events(self):
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

    def _update(self):
        if not self.snake.move():
            return False
        head = self.snake.positions[0]
        for apple in self._all_apples():
            if head == apple.position:
                self.score += apple.on_eat(self.snake)
                if not self.snake.positions:
                    return False
                apple.respawn(self._obstacles_excluding(apple))
                break
        return True

    def _draw(self):
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
        score_text = self.font.render(
            f"Score: {self.score}", True, SCORE_COLOR
        )
        self.screen.blit(score_text, (10, 10))

    def _show_end_screen(self, title):
        self.screen.fill(BACKGROUND_COLOR)
        title_surf = self.font.render(title, True, SCORE_COLOR)
        score_surf = self.font.render(
            f"Score: {self.score}", True, SCORE_COLOR
        )
        restart_surf = self.font.render(
            "Press Space to Restart", True, SCORE_COLOR
        )
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

    def _wait_for_restart(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif (
                    event.type == pygame.KEYDOWN
                    and event.key == pygame.K_SPACE
                ):
                    self._reset()
                    return
