"""
algorithms.py - Depth-First Search (DFS) and Breadth-First Search (BFS)
Part of the DAA College Mini-Project: Maze Game Using Basic DSA Algorithms.

This module implements two fundamental graph search algorithms:
1. Depth-First Search (DFS) using a LIFO Stack
2. Breadth-First Search (BFS) using a FIFO Queue

Both algorithms operate on the 2D grid generated in maze.py and record:
- The order in which nodes are visited (for step-by-step visual animation).
- The final path reconstructed from the exit back to the start.
- Quantitative metrics: number of nodes explored, path length, and execution time (ms).
"""

import time
from collections import deque


class SearchResult:
    """
    Encapsulates the performance metrics and results of a graph search algorithm.
    """

    def __init__(self, algorithm_name, path, explored_order, execution_time_ms, nodes_explored, is_optimal):
        self.algorithm_name = algorithm_name
        self.path = path                              # Reconstructed path from start to exit
        self.explored_order = explored_order          # Sequence of visited nodes (for animation)
        self.execution_time_ms = execution_time_ms    # Elapsed algorithm runtime in ms
        self.nodes_explored = nodes_explored          # Total nodes visited during search
        self.path_length = len(path) if path else 0   # Number of cells in solution path
        self.is_optimal = is_optimal                  # True if shortest path is mathematically guaranteed
        self.found = bool(path)                       # True if a valid path to exit was found

    def __repr__(self):
        return (
            f"SearchResult(algorithm={self.algorithm_name}, "
            f"found={self.found}, "
            f"nodes_explored={self.nodes_explored}, "
            f"path_length={self.path_length}, "
            f"time={self.execution_time_ms:.4f}ms, "
            f"optimal={self.is_optimal})"
        )


def reconstruct_path(parent_map, start_pos, exit_pos):
    """
    Reconstruct the path from start_pos to exit_pos using the parent map.

    Parameters:
        parent_map (dict): Mapping from child cell (r, c) to parent cell (pr, pc).
        start_pos (tuple): (row, col) of start.
        exit_pos (tuple): (row, col) of exit.

    Returns:
        list of tuple: Path of (r, c) coordinates from start_pos to exit_pos.
    """
    if exit_pos not in parent_map and exit_pos != start_pos:
        return []

    path = []
    curr = exit_pos
    while curr is not None:
        path.append(curr)
        curr = parent_map.get(curr)

    path.reverse()  # Reverse to get order from start -> exit
    return path


def solve_dfs(maze, start_pos=None, exit_pos=None):
    """
    Solve the maze using Depth-First Search (DFS).

    DATA STRUCTURE USED:
    - Stack (LIFO: Last-In, First-Out).
    - In Python, a standard list is used as a stack:
        * stack.append(item) -> push operation
        * stack.pop()        -> pop operation

    ALGORITHM LOGIC:
    1. Initialize an empty stack and push the start cell.
    2. Maintain a `visited` set to avoid revisiting cells and avoid infinite loops.
    3. Maintain a `parent` dictionary to record which cell led to which neighbor.
    4. While the stack is not empty:
       a. Pop the top cell from the stack.
       b. If it was already visited, skip it.
       c. Mark as visited and record in `explored_order`.
       d. If the current cell is the exit cell, terminate search.
       e. For each walkable 4-directional neighbor:
          - If the neighbor has not been visited:
            * Record parent[neighbor] = current
            * Push neighbor onto the stack.
    5. Reconstruct the path from exit to start using parent pointers.

    DAA CHARACTERISTICS:
    - DFS dives deep along one corridor until hitting a dead end, then backtracks.
    - Time Complexity: O(V + E) where V = rows * cols and E <= 4 * V.
    - Space Complexity: O(V) for the stack and visited set.
    - Optimality: Does NOT guarantee the shortest path. It returns the first path it finds.

    Returns:
        SearchResult: Contains path, explored sequence, and benchmark metrics.
    """
    start = start_pos if start_pos is not None else maze.start_pos
    target = exit_pos if exit_pos is not None else maze.exit_pos

    start_time = time.perf_counter()

    stack = [start]
    visited = set()
    parent = {start: None}
    explored_order = []
    found = False

    while stack:
        curr = stack.pop()

        if curr in visited:
            continue

        visited.add(curr)
        explored_order.append(curr)

        # Check if exit is reached
        if curr == target:
            found = True
            break

        # Explore neighbors
        # (Order: Up, Down, Left, Right or reverse for directional preference)
        for neighbor in maze.get_neighbors(curr[0], curr[1]):
            if neighbor not in visited:
                if neighbor not in parent:
                    parent[neighbor] = curr
                stack.append(neighbor)

    elapsed_ms = (time.perf_counter() - start_time) * 1000.0

    path = reconstruct_path(parent, start, target) if found else []

    return SearchResult(
        algorithm_name="Depth-First Search (DFS)",
        path=path,
        explored_order=explored_order,
        execution_time_ms=elapsed_ms,
        nodes_explored=len(explored_order),
        is_optimal=False
    )


def solve_bfs(maze, start_pos=None, exit_pos=None):
    """
    Solve the maze using Breadth-First Search (BFS).

    DATA STRUCTURE USED:
    - Queue (FIFO: First-In, First-Out).
    - In Python, `collections.deque` is used as an efficient O(1) queue:
        * queue.append(item)    -> enqueue operation
        * queue.popleft()       -> dequeue operation

    ALGORITHM LOGIC:
    1. Initialize an empty queue and enqueue the start cell.
    2. Maintain a `visited` set and mark the start cell as visited immediately.
    3. Maintain a `parent` dictionary to record which cell led to which neighbor.
    4. While the queue is not empty:
       a. Dequeue the front cell from the queue.
       b. Record the dequeued cell in `explored_order`.
       c. If the current cell is the exit cell, terminate search.
       d. For each walkable 4-directional neighbor:
          - If the neighbor has not been visited:
            * Mark neighbor as visited immediately (prevents duplicate enqueues).
            * Record parent[neighbor] = current.
            * Enqueue neighbor into the queue.
    5. Reconstruct the shortest path from exit to start using parent pointers.

    DAA CHARACTERISTICS:
    - BFS explores level-by-level in expanding concentric rings.
    - Time Complexity: O(V + E) where V = rows * cols and E <= 4 * V.
    - Space Complexity: O(V) for the queue and visited set.
    - Optimality: GUARANTEED to find the shortest path in any unweighted graph/grid,
      because it visits all nodes at distance k before any node at distance k + 1.

    Returns:
        SearchResult: Contains path, explored sequence, and benchmark metrics.
    """
    start = start_pos if start_pos is not None else maze.start_pos
    target = exit_pos if exit_pos is not None else maze.exit_pos

    start_time = time.perf_counter()

    queue = deque([start])
    visited = {start}
    parent = {start: None}
    explored_order = []
    found = False

    while queue:
        curr = queue.popleft()
        explored_order.append(curr)

        # Check if exit is reached
        if curr == target:
            found = True
            break

        # Explore neighbors
        for neighbor in maze.get_neighbors(curr[0], curr[1]):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = curr
                queue.append(neighbor)

    elapsed_ms = (time.perf_counter() - start_time) * 1000.0

    path = reconstruct_path(parent, start, target) if found else []

    return SearchResult(
        algorithm_name="Breadth-First Search (BFS)",
        path=path,
        explored_order=explored_order,
        execution_time_ms=elapsed_ms,
        nodes_explored=len(explored_order),
        is_optimal=True
    )
