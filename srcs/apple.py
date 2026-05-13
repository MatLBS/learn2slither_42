import random
import pygame
from srcs.constants import (
    CELL_SIZE,
    GRID_SIZE,
    GREEN_APPLE_COLOR,
    RED_APPLE_COLOR,
)
from srcs.snake import Snake


class Apple:
    color = GREEN_APPLE_COLOR

    def __init__(self, forbidden: list):
        self.position = self._random_position(forbidden)

    def _random_position(self, forbidden: list) -> tuple[int, int]:
        forbidden_set = set(forbidden)
        while True:
            position = (
                random.randint(1, GRID_SIZE - 2),
                random.randint(1, GRID_SIZE - 2),
            )
            if position not in forbidden_set:
                return position

    def respawn(self, forbidden: list) -> None:
        self.position = self._random_position(forbidden)

    def on_eat(self, snake: Snake) -> int:
        snake.grow_snake()
        return 1

    def draw(self, surface: pygame.Surface) -> None:
        rect = pygame.Rect(
            self.position[0] * CELL_SIZE,
            self.position[1] * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE,
        )
        pygame.draw.rect(surface, self.color, rect)


class RedApple(Apple):
    color = RED_APPLE_COLOR

    def on_eat(self, snake: Snake) -> int:
        snake.shrink_snake()
        return 0
