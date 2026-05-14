import random
import pygame
from srcs.constants import SNAKE_COLOR


class Snake:
    def __init__(self, grid_size: int, cell_size: int):
        self.grid_size = grid_size
        self.cell_size = cell_size
        self._random_start()
        self._grow = False

    def _random_start(self) -> None:
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        self.direction = random.choice(directions)
        dx, dy = self.direction

        x_min = 1 + max(0, 2 * dx)
        x_max = self.grid_size - 2 + min(0, 2 * dx)
        y_min = 1 + max(0, 2 * dy)
        y_max = self.grid_size - 2 + min(0, 2 * dy)

        head_x = random.randint(x_min, x_max)
        head_y = random.randint(y_min, y_max)

        self.positions = [(head_x - i * dx, head_y - i * dy) for i in range(3)]

    def move(self) -> bool:
        head_x, head_y = self.positions[0]
        delta_x, delta_y = self.direction
        new_head = (head_x + delta_x, head_y + delta_y)

        in_bounds = (
            1 <= new_head[0] < self.grid_size - 1
            and 1 <= new_head[1] < self.grid_size - 1
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
        cs = self.cell_size
        for x, y in self.positions:
            rect = pygame.Rect(x * cs, y * cs, cs, cs)
            pygame.draw.rect(surface, SNAKE_COLOR, rect)

        if not self.positions:
            return
        head_x, head_y = self.positions[0]
        eye_size = cs // 5
        eye_y_offset = cs // 3
        eye_x_inset = cs // 6
        eye_y = head_y * cs + eye_y_offset
        eye1 = pygame.Rect(head_x * cs + eye_x_inset, eye_y, eye_size, eye_size)
        eye2 = pygame.Rect(
            (head_x + 1) * cs - eye_x_inset - eye_size,
            eye_y,
            eye_size,
            eye_size,
        )
        pygame.draw.rect(surface, (0, 0, 0), eye1)
        pygame.draw.rect(surface, (0, 0, 0), eye2)
