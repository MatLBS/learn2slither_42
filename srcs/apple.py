import random
import pygame
from srcs.constants import CELL_SIZE, GRID_SIZE, APPLE_COLOR


class Apple:
    def __init__(self, snake):
        self.position = self._random_position(snake)

    def _random_position(self, snake):
        while True:
            position = (
                random.randint(1, GRID_SIZE - 2),
                random.randint(1, GRID_SIZE - 2),
            )
            if position not in snake.positions:
                return position

    def respawn(self, snake):
        self.position = self._random_position(snake)

    def draw(self, surface):
        rect = pygame.Rect(
            self.position[0] * CELL_SIZE,
            self.position[1] * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE,
        )
        pygame.draw.rect(surface, APPLE_COLOR, rect)
