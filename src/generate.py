import random
from typing import Any, Callable
import pygame

from .animations import AnimatingNode, Animation, Animator
from .constants import CELL_SIZE, DARK, GREEN_2, BLUE_2, MIN_SIZE, WHITE


GenerationCallback = Callable[[], None]


class MazeGenerator:

    def __init__(self, animator: Animator) -> None:
        from .maze import Maze

        self.animator = animator
        self.maze: Maze = animator.maze

    def _is_valid_cell(self, pos: tuple[int, int]) -> bool:
        """Check if the provided coords are valid

        Args:
            pos (tuple[int, int]): Cell pos

        Returns:
            bool: Whether the cell exists
        """
        rowIdx, colIdx = pos

        return 0 <= rowIdx < self.maze.height \
            and 0 <= colIdx < self.maze.width

    def _get_two_step_neighbors(
        self,
        maze: list[list[Any]],
        cell: tuple[int, int],
        value: str = ""
    ) -> list[tuple[int, int]]:
        """Get neighbors of a cell which are two steps away

        Args:
            cell (tuple[int, int]): Cell pos
            value (str): A string representing the neighbor type. `#` for a wall

        Returns:
            list[tuple[int, int]]: List of neighbors
        """
        neighbors = [(cell[0] + 2, cell[1]),
                     (cell[0] - 2, cell[1]),
                     (cell[0], cell[1] + 2),
                     (cell[0], cell[1] - 2)]

        if value == "#":
            return [neighbor for neighbor in neighbors
                    if self._is_valid_cell(neighbor)
                    and maze[neighbor[0]][neighbor[1]] == "#"]
        elif value == "1":
            return [neighbor for neighbor in neighbors
                    if self._is_valid_cell(neighbor)
                    and maze[neighbor[0]][neighbor[1]] != "#"]

        return [neighbor for neighbor in neighbors
                if self._is_valid_cell(neighbor)]

    

    def basic_weight_maze(self) -> None:
        """Generate a basic weight maze
        """

        nodes = []
        for rowIdx in range(self.maze.width):
            for colIdx in range(self.maze.height):
                if random.randint(1, 10) < 8:
                    continue

                x, y = self.maze.coords[colIdx][rowIdx]
                nodes.append(
                    AnimatingNode(
                        rect=pygame.Rect(0, 0, MIN_SIZE, MIN_SIZE),
                        center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2),
                        ticks=pygame.time.get_ticks(),
                        value="9",
                        color=WHITE,
                        animation=Animation.WEIGHT_ANIMATION
                    )
                )

        self.maze.animator.add_nodes_to_animate(nodes, gap=2)

    def basic_random_maze(self) -> None:
        """Generate a basic random maze
        """
        nodes = []
        for rowIdx in range(self.maze.width):
            for colIdx in range(self.maze.height):
                if random.randint(1, 10) < 8:
                    continue

                x, y = self.maze.coords[colIdx][rowIdx]
                nodes.append(
                    AnimatingNode(
                        rect=pygame.Rect(0, 0, MIN_SIZE, MIN_SIZE),
                        center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2),
                        ticks=pygame.time.get_ticks(),
                        value="#",
                        color=DARK
                    )
                )

        self.maze.animator.add_nodes_to_animate(nodes, gap=2)

    
    def _draw_line(
        self,
        x1: int,
        x2: int,
        y1: int,
        y2: int,
        horizontal: bool = False
    ) -> int:
        """Draw walls horizontally or vertically

        Args:
            x1 (int): Grid row start
            x2 (int): Grid row end
            y1 (int): Grid column start
            y2 (int): Grid column end
            horizontal (bool, optional): Horizontal or vertical. Defaults to False.

        Returns:
            int: X or Y coordinate of wall line
        """

        # Handle horizontal division
        if horizontal:
            x1, y1 = y1, x1
            x2, y2 = y2, x2

        # Walls at even places
        if x1 % 2 != 0:
            x1 += 1
        wall = random.randrange(x1, x2, 2)

        # Holes at odd places
        if y1 % 2 == 0:
            y1 += 1
        hole = random.randrange(y1, y2, 2)

        # Coordinates
        hole_coords = (hole, wall) if not horizontal else (wall, hole)
        wall_coords = [-1, wall] if not horizontal else [wall, -1]

        # Draw walls
        nodes_to_animate = []
        for i in range(y1, y2 + 1):
            wall_coords[horizontal] = i
            if hole_coords == tuple(wall_coords):
                continue

            # Create a rectangle
            rect = pygame.Rect(0, 0, MIN_SIZE, MIN_SIZE)

            # Set the starting position of the rectangle
            x, y = self.maze.coords[wall_coords[0]][wall_coords[1]]
            rect.center = (x + CELL_SIZE // 2, y + CELL_SIZE // 2)
            nodes_to_animate.append(
                AnimatingNode(
                    center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2),
                    rect=rect,
                    ticks=pygame.time.get_ticks(),
                    value="#",
                    color=DARK
                )
            )
        self.maze.animator.add_nodes_to_animate(nodes_to_animate)

        return wall
