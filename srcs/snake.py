import random
import pygame
from srcs.constants import CELL_SIZE, GRID_SIZE, SNAKE_COLOR


class Snake:
    def __init__(self):
        self._random_start()
        self._grow = False

    def _random_start(self) -> None:
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        self.direction = random.choice(directions)
        dx, dy = self.direction

        x_min = 1 + max(0, 2 * dx)
        x_max = GRID_SIZE - 2 + min(0, 2 * dx)
        y_min = 1 + max(0, 2 * dy)
        y_max = GRID_SIZE - 2 + min(0, 2 * dy)

        head_x = random.randint(x_min, x_max)
        head_y = random.randint(y_min, y_max)

        self.positions = [(head_x - i * dx, head_y - i * dy) for i in range(3)]

    def move(self) -> bool:
        head_x, head_y = self.positions[0]
        delta_x, delta_y = self.direction
        new_head = (head_x + delta_x, head_y + delta_y)

        in_bounds = (
            1 <= new_head[0] < GRID_SIZE - 1 and 1 <= new_head[1] < GRID_SIZE - 1
        )
        if new_head in self.positions or not in_bounds:
            return False

        self.positions.insert(0, new_head)

        if not self._grow:
            self.positions.pop()
        else:
            self._grow = False

        return True

    def change_direction(self, direction: tuple[int, int]) -> None:
        opposite = (-self.direction[0], -self.direction[1])
        if direction != opposite:
            self.direction = direction

    def grow_snake(self) -> None:
        self._grow = True

    def shrink_snake(self) -> None:
        if self.positions:
            self.positions.pop()

    def draw(self, surface: pygame.Surface) -> None:
        for x, y in self.positions:
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, SNAKE_COLOR, rect)

        if not self.positions:
            return
        head_x, head_y = self.positions[0]
        eye_size = CELL_SIZE // 5
        eye_y_offset = CELL_SIZE // 3
        eye_x_inset = CELL_SIZE // 6
        eye_y = head_y * CELL_SIZE + eye_y_offset
        eye1 = pygame.Rect(head_x * CELL_SIZE + eye_x_inset, eye_y, eye_size, eye_size)
        eye2 = pygame.Rect(
            (head_x + 1) * CELL_SIZE - eye_x_inset - eye_size,
            eye_y,
            eye_size,
            eye_size,
        )
        pygame.draw.rect(surface, (0, 0, 0), eye1)
        pygame.draw.rect(surface, (0, 0, 0), eye2)
