"""
maze.py - Maze Generation and Grid Management
Part of the DAA College Mini-Project: Maze Game Using Basic DSA Algorithms.

This module represents the maze as a 2D grid (list of lists) and implements
procedural maze generation using Randomized Depth-First Search (Recursive Backtracker).
It guarantees that there is always at least one valid walkable path from the
start cell to the exit cell.
"""

import random


# Cell Type Constants
PATH = 0   # Open walkable corridor
WALL = 1   # Impassable obstacle wall


class Maze:
    """
    Manages the 2D grid representation of the maze, wall collisions,
    and procedural maze generation.
    """

    def __init__(self, rows=21, cols=21, braid_prob=0.08, seed=None):
        """
        Initialize the maze dimensions and generate an initial solvable maze.

        Parameters:
            rows (int): Number of grid rows (recommended odd number, e.g. 21).
            cols (int): Number of grid columns (recommended odd number, e.g. 21).
            braid_prob (float): Probability of removing internal dead-end walls.
                                Adding loops (braiding) creates alternate routes,
                                clearly demonstrating BFS shortest-path vs DFS path.
            seed (int, optional): Random seed for reproducible maze generation.
        """
        # Ensure dimensions are odd for proper grid wall-corridor spacing
        self.rows = rows if rows % 2 == 1 else rows + 1
        self.cols = cols if cols % 2 == 1 else cols + 1
        self.braid_prob = braid_prob

        if seed is not None:
            random.seed(seed)

        # Standard start and exit positions (inside grid boundary)
        self.start_pos = (1, 1)
        self.exit_pos = (self.rows - 2, self.cols - 2)

        # 2D list representing the maze grid: grid[row][col]
        self.grid = []
        self.generate()

    def generate(self):
        """
        Generate a random solvable maze using the Randomized DFS / Recursive
        Backtracker algorithm on a 2D grid.

        Algorithm Steps:
        1. Fill the entire 2D grid with WALLs (1).
        2. Start at cell (1, 1), carve it as a PATH (0), and push it to a stack.
        3. While the stack is not empty:
           a. Pop or peek the current cell.
           b. Find all unvisited neighbors at distance 2 (skipping the wall in between).
           c. If unvisited neighbors exist:
              - Randomly pick one neighbor.
              - Carve out the wall between current cell and chosen neighbor.
              - Carve out the neighbor cell.
              - Push neighbor to stack.
           d. If no unvisited neighbors exist, backtrack (pop from stack).
        4. Ensure start and exit cells are open corridors.
        5. Optionally remove a small fraction of internal walls to create loops
           so that BFS and DFS can showcase differing path lengths.
        """
        # Step 1: Initialize the entire grid as walls
        self.grid = [[WALL for _ in range(self.cols)] for _ in range(self.rows)]

        # Step 2: Randomized Depth-First Search with Stack
        stack = []
        visited = set()

        start_r, start_c = self.start_pos
        self.grid[start_r][start_c] = PATH
        visited.add((start_r, start_c))
        stack.append((start_r, start_c))

        # Movement vectors for distance-2 neighbors: Up, Down, Left, Right
        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]

        while stack:
            curr_r, curr_c = stack[-1]

            # Find all valid unvisited neighbors at distance 2
            unvisited_neighbors = []
            for dr, dc in directions:
                nr, nc = curr_r + dr, curr_c + dc
                if 1 <= nr < self.rows - 1 and 1 <= nc < self.cols - 1:
                    if (nr, nc) not in visited:
                        unvisited_neighbors.append((nr, nc, dr, dc))

            if unvisited_neighbors:
                # Randomly pick an unvisited neighbor
                nr, nc, dr, dc = random.choice(unvisited_neighbors)

                # Knock down the wall between current cell and the neighbor
                wall_r = curr_r + dr // 2
                wall_c = curr_c + dc // 2
                self.grid[wall_r][wall_c] = PATH
                self.grid[nr][nc] = PATH

                visited.add((nr, nc))
                stack.append((nr, nc))
            else:
                # Backtrack when dead end is reached
                stack.pop()

        # Step 3: Explicitly guarantee start and exit are open
        self.grid[self.start_pos[0]][self.start_pos[1]] = PATH
        self.grid[self.exit_pos[0]][self.exit_pos[1]] = PATH

        # Step 4: Add braiding (create alternate routes/cycles)
        # In a strict tree maze, there is only 1 path between any two points.
        # Adding a few loops allows BFS to find shorter routes while DFS explores detours.
        if self.braid_prob > 0:
            self._add_loops(self.braid_prob)

    def _add_loops(self, probability):
        """
        Randomly remove a few internal walls to introduce alternate paths and cycles.
        """
        for r in range(2, self.rows - 2, 2):
            for c in range(2, self.cols - 2, 2):
                if self.grid[r][c] == WALL and random.random() < probability:
                    # Check if removing this wall connects two existing paths
                    horizontal = (self.grid[r][c - 1] == PATH and self.grid[r][c + 1] == PATH)
                    vertical = (self.grid[r - 1][c] == PATH and self.grid[r + 1][c] == PATH)
                    if horizontal or vertical:
                        self.grid[r][c] = PATH

    def is_valid_move(self, r, c):
        """
        Check if moving to cell (r, c) is legal (within bounds and not a wall).

        Parameters:
            r (int): Target row.
            c (int): Target column.

        Returns:
            bool: True if cell is walkable, False if wall or outside boundary.
        """
        if 0 <= r < self.rows and 0 <= c < self.cols:
            return self.grid[r][c] == PATH
        return False

    def get_neighbors(self, r, c):
        """
        Get all walkable 4-directional adjacent neighbors of cell (r, c).

        Returns:
            list of tuple: List of (neighbor_r, neighbor_c) valid path coordinates.
        """
        neighbors = []
        # Standard 4 directions: Up, Down, Left, Right
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if self.is_valid_move(nr, nc):
                neighbors.append((nr, nc))
        return neighbors

    def to_ascii(self):
        """
        Return an ASCII string representation of the maze for testing or CLI display.
        '#' = Wall, ' ' = Path, 'S' = Start, 'E' = Exit.
        """
        lines = []
        for r in range(self.rows):
            row_str = []
            for c in range(self.cols):
                if (r, c) == self.start_pos:
                    row_str.append("S")
                elif (r, c) == self.exit_pos:
                    row_str.append("E")
                elif self.grid[r][c] == WALL:
                    row_str.append("#")
                else:
                    row_str.append(" ")
            lines.append("".join(row_str))
        return "\n".join(lines)
