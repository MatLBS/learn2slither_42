import random
import pygame
from srcs.constants import (
    GREEN_APPLE_COLOR,
    RED_APPLE_COLOR,
)
from srcs.snake import Snake


class Apple:
    color = GREEN_APPLE_COLOR

    def __init__(self, forbidden: list, grid_size: int, cell_size: int):
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.position = self._random_position(forbidden)

    def _random_position(self, forbidden: list) -> tuple[int, int]:
        forbidden_set = set(forbidden)
        while True:
            position = (
                random.randint(1, self.grid_size - 2),
                random.randint(1, self.grid_size - 2),
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
            self.position[0] * self.cell_size,
            self.position[1] * self.cell_size,
            self.cell_size,
            self.cell_size,
        )
        pygame.draw.rect(surface, self.color, rect)


class RedApple(Apple):
    color = RED_APPLE_COLOR

    def on_eat(self, snake: Snake) -> int:
        snake.shrink_snake()
        return 0
