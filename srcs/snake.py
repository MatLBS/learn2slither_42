import pygame
from srcs.constants import CELL_SIZE, GRID_SIZE, SNAKE_COLOR


class Snake:
    def __init__(self):
        self.positions = [(5, 5), (4, 5), (3, 5)]
        self.direction = (1, 0)
        self._grow = False

    def move(self):
        head_x, head_y = self.positions[0]
        delta_x, delta_y = self.direction
        new_head = (head_x + delta_x, head_y + delta_y)

        in_bounds = (
            1 <= new_head[0] < GRID_SIZE - 1
            and 1 <= new_head[1] < GRID_SIZE - 1
        )
        if new_head in self.positions or not in_bounds:
            return False

        self.positions.insert(0, new_head)

        if not self._grow:
            self.positions.pop()
        else:
            self._grow = False

        return True

    def change_direction(self, direction):
        opposite = (-self.direction[0], -self.direction[1])
        if direction != opposite:
            self.direction = direction

    def grow_snake(self):
        self._grow = True

    def draw(self, surface):
        for x, y in self.positions:
            rect = pygame.Rect(
                x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE
            )
            pygame.draw.rect(surface, SNAKE_COLOR, rect)

        head_x, head_y = self.positions[0]
        eye1 = pygame.Rect(
            head_x * CELL_SIZE + 8, head_y * CELL_SIZE + 8, 5, 5
        )
        eye2 = pygame.Rect(
            head_x * CELL_SIZE + 17, head_y * CELL_SIZE + 8, 5, 5
        )
        pygame.draw.rect(surface, (0, 0, 0), eye1)
        pygame.draw.rect(surface, (0, 0, 0), eye2)
