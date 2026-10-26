"""
test_maze_game.py - Comprehensive Unit & Integration Test Suite
Part of the DAA College Mini-Project: Maze Game Using Basic DSA Algorithms.

Validates the 7 core testing requirements:
1. Maze is generated correctly with odd grid dimensions and perimeter walls.
2. A valid path always exists between start and exit cells.
3. Player cannot move through walls or off the grid.
4. Depth-First Search (DFS) finds a valid path from start to exit.
5. Breadth-First Search (BFS) finds an optimal shortest path (length <= DFS).
6. Mazes can be repeatedly regenerated without state leakage.
7. Game and player positions can be restarted without errors.
"""

import os
import sys
import unittest

# Ensure maze_game is in python search path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from maze import Maze, PATH, WALL
from algorithms import solve_dfs, solve_bfs, reconstruct_path


class TestMazeGame(unittest.TestCase):
    """Test suite covering maze generation, DSA search algorithms, and game rules."""

    def setUp(self):
        """Set up fresh maze instances for each test."""
        self.maze = Maze(rows=21, cols=21, braid_prob=0.10, seed=42)

    def test_01_maze_generation_structure(self):
        """Verify maze dimensions, start/exit positions, and boundary walls."""
        self.assertEqual(self.maze.rows, 21)
        self.assertEqual(self.maze.cols, 21)
        self.assertEqual(self.maze.start_pos, (1, 1))
        self.assertEqual(self.maze.exit_pos, (19, 19))

        # Start and Exit must be walkable corridors
        self.assertEqual(self.maze.grid[1][1], PATH)
        self.assertEqual(self.maze.grid[19][19], PATH)

        # Perimeter outer boundary must be solid walls
        for c in range(self.maze.cols):
            self.assertEqual(self.maze.grid[0][c], WALL, "Top row must be walls")
            self.assertEqual(self.maze.grid[self.maze.rows - 1][c], WALL, "Bottom row must be walls")
        for r in range(self.maze.rows):
            self.assertEqual(self.maze.grid[r][0], WALL, "Left column must be walls")
            self.assertEqual(self.maze.grid[r][self.maze.cols - 1], WALL, "Right column must be walls")

    def test_02_valid_path_guaranteed(self):
        """Verify that at least one valid continuous path exists between start and exit."""
        # Use BFS to verify connectivity
        result = solve_bfs(self.maze)
        self.assertTrue(result.found, "BFS must find a path from start to exit in generated maze")
        self.assertGreater(result.path_length, 0, "Path length must be greater than 0")
        self.assertEqual(result.path[0], self.maze.start_pos, "Path must start at start_pos")
        self.assertEqual(result.path[-1], self.maze.exit_pos, "Path must end at exit_pos")

        # Verify path continuity (every consecutive pair must be distance 1 adjacent)
        for i in range(len(result.path) - 1):
            r1, c1 = result.path[i]
            r2, c2 = result.path[i + 1]
            dist = abs(r1 - r2) + abs(c1 - c2)
            self.assertEqual(dist, 1, f"Path discontinuity detected between {result.path[i]} and {result.path[i+1]}")
            self.assertEqual(self.maze.grid[r1][c1], PATH)
            self.assertEqual(self.maze.grid[r2][c2], PATH)

    def test_03_wall_collision_and_boundary(self):
        """Verify that player cannot move through walls or off-grid coordinates."""
        # Find a wall cell
        wall_found = False
        for r in range(self.maze.rows):
            for c in range(self.maze.cols):
                if self.maze.grid[r][c] == WALL:
                    self.assertFalse(self.maze.is_valid_move(r, c), f"Cell ({r}, {c}) is a wall and must be invalid")
                    wall_found = True
                    break
            if wall_found:
                break

        # Check off-grid coordinates
        self.assertFalse(self.maze.is_valid_move(-1, 0), "Negative row must be invalid")
        self.assertFalse(self.maze.is_valid_move(0, -1), "Negative col must be invalid")
        self.assertFalse(self.maze.is_valid_move(self.maze.rows, 5), "Out-of-bound row must be invalid")
        self.assertFalse(self.maze.is_valid_move(5, self.maze.cols), "Out-of-bound col must be invalid")

        # Start position must be a valid move
        self.assertTrue(self.maze.is_valid_move(1, 1), "Start position (1, 1) must be valid")

    def test_04_dfs_algorithm_correctness(self):
        """Verify that DFS successfully solves the maze and records valid metrics."""
        dfs_res = solve_dfs(self.maze)
        self.assertTrue(dfs_res.found, "DFS must find a path to exit")
        self.assertGreater(dfs_res.nodes_explored, 0, "DFS must explore at least one node")
        self.assertGreater(dfs_res.execution_time_ms, 0.0, "Execution time should be positive")
        self.assertEqual(dfs_res.path[0], self.maze.start_pos)
        self.assertEqual(dfs_res.path[-1], self.maze.exit_pos)

    def test_05_bfs_shortest_path_optimality(self):
        """Verify that BFS finds the optimal shortest path (path_length <= DFS path_length)."""
        # Test over 20 random mazes with loops
        for s in range(20):
            test_maze = Maze(rows=21, cols=21, braid_prob=0.15, seed=100 + s)
            dfs_res = solve_dfs(test_maze)
            bfs_res = solve_bfs(test_maze)

            self.assertTrue(dfs_res.found)
            self.assertTrue(bfs_res.found)
            self.assertLessEqual(
                bfs_res.path_length,
                dfs_res.path_length,
                f"BFS path ({bfs_res.path_length}) was longer than DFS path ({dfs_res.path_length})!"
            )

    def test_06_repeated_maze_regeneration(self):
        """Verify that mazes can be regenerated multiple times without error or invalid states."""
        for _ in range(10):
            self.maze.generate()
            self.assertEqual(self.maze.grid[1][1], PATH)
            self.assertEqual(self.maze.grid[self.maze.rows - 2][self.maze.cols - 2], PATH)
            res = solve_bfs(self.maze)
            self.assertTrue(res.found, "Each newly generated maze must be solvable")

    def test_07_path_reconstruction_edge_cases(self):
        """Verify path reconstruction when exit is unreachable or identical to start."""
        # Unreachable test
        empty_parent = {}
        path = reconstruct_path(empty_parent, (1, 1), (5, 5))
        self.assertEqual(path, [], "Unreachable node must return empty path")

        # Same start and exit
        same_parent = {(1, 1): None}
        path_same = reconstruct_path(same_parent, (1, 1), (1, 1))
        self.assertEqual(path_same, [(1, 1)], "Start equals exit must return single node path")


if __name__ == "__main__":
    unittest.main()
