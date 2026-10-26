# DAA College Mini-Project: Viva Questions and Model Answers

## Course: Design and Analysis of Algorithms (DAA)
### Project: Maze Game Using Basic DSA Algorithms in Python (DFS vs BFS)

This document contains **25 essential viva and presentation questions** with clear, technically precise answers tailored for third-year computer science / information technology engineering students.

---

### Section 1: Core Problem & Grid Representation

#### Q1: What is the main objective of this project?
**Answer:**  
The main objective is to design an interactive, educational maze game using Python and Pygame that models mazes as unweighted graphs. It allows a human player to solve the maze manually while demonstrating, visualizing, and empirically benchmarking two fundamental graph traversal algorithms: Depth-First Search (DFS) using a stack and Breadth-First Search (BFS) using a queue.

#### Q2: How is the maze represented in Python data structures?
**Answer:**  
The maze is represented as a 2D grid matrix using a list of lists: `grid[row][col]`.  
- `grid[r][c] == 0` represents an open walkable **PATH** (a graph vertex).
- `grid[r][c] == 1` represents an impassable solid **WALL** (an obstacle).  
Edges exist between adjacent cells $(r_1, c_1)$ and $(r_2, c_2)$ if their Manhattan distance is 1 ($|r_1 - r_2| + |c_1 - c_2| = 1$) and both cells are walkable paths.

#### Q3: Why are odd dimensions (e.g. $21 \times 21$) used for the maze?
**Answer:**  
In grid-based maze generation algorithms like the Recursive Backtracker, cells at odd coordinates $(2i + 1, 2j + 1)$ represent path chambers, while cells at even coordinates represent walls between them. Odd dimensions ensure that the maze has a solid perimeter of outer boundary walls on all four sides with no open borders leaking outside the grid.

#### Q4: How do you prevent the player from walking through walls?
**Answer:**  
Before moving the player from `(r, c)` to `(r + dr, c + dc)`, the game checks the target coordinates with `maze.is_valid_move(r + dr, c + dc)`. This function verifies two boundary invariants:
1. The row and column indices lie within bounds ($0 \le r < \text{rows}$ and $0 \le c < \text{cols}$).
2. The cell value equals `PATH` (`0`). If the cell is `WALL` (`1`), the movement event is ignored.

---

### Section 2: Maze Generation Algorithm

#### Q5: How is the maze generated procedurally?
**Answer:**  
The maze is generated using the **Randomized Depth-First Search (Recursive Backtracker)** algorithm:
1. All cells in the 2D grid are initially marked as `WALL` (`1`).
2. Starting at cell `(1, 1)`, we carve it as a `PATH` (`0`) and push it onto a stack.
3. While the stack is not empty:
   - Inspect unvisited neighbors at step distance 2.
   - If unvisited neighbors exist, randomly select one, knock down the intermediate wall between them, carve the neighbor as `PATH`, and push it onto the stack.
   - If no unvisited neighbors exist, pop the top cell from the stack (backtrack).
4. Finally, verify that `start_pos = (1, 1)` and `exit_pos = (rows-2, cols-2)` are open.

#### Q6: How do you guarantee that a valid path always exists from start to exit?
**Answer:**  
The Recursive Backtracker algorithm generates a **Spanning Tree** of the grid graph. By definition, a spanning tree connects every reachable cell in the maze with zero disconnected partitions. Because both `(1, 1)` and `(rows - 2, cols - 2)` belong to this connected tree component, a valid continuous path between them is mathematically guaranteed.

#### Q7: What is "braiding" and why did you add it to the maze generator?
**Answer:**  
A pure spanning tree maze has no cycles (loops), meaning there is strictly *one unique path* between any two cells. In a tree maze, BFS and DFS would eventually return the exact same final path.  
By removing a small percentage (e.g. 10%) of additional internal walls ("braiding"), we introduce loops and alternate routes. This allows us to dramatically illustrate the difference between BFS (which takes the shorter, direct path) and DFS (which can take a longer, convoluted detour).

---

### Section 3: Data Structures (Stacks vs Queues)

#### Q8: What data structure does DFS use, and what is its traversal principle?
**Answer:**  
DFS uses a **Stack** operating on the **LIFO (Last-In, First-Out)** principle. The most recently discovered neighbor is pushed onto the stack and popped first. This causes DFS to aggressively plunge deep down a single corridor until hitting a dead end before backtracking.

#### Q9: What data structure does BFS use, and what is its traversal principle?
**Answer:**  
BFS uses a **Queue** operating on the **FIFO (First-In, First-Out)** principle. Newly discovered neighbors are appended to the back of the queue, and nodes are processed in the exact order they were discovered. This produces a level-by-level, concentric expansion outward from the start node.

#### Q10: Why did you use `collections.deque` instead of a standard Python list for BFS?
**Answer:**  
In Python, using `list.pop(0)` for a queue takes $\mathcal{O}(N)$ linear time because all subsequent elements in memory must be shifted left by one position. In contrast, `collections.deque.popleft()` takes $\mathcal{O}(1)$ constant time because it is implemented internally as a doubly-linked list of memory blocks. This keeps BFS time complexity strictly linear $\mathcal{O}(V + E)$.

#### Q11: What is the purpose of the `visited` set in both algorithms?
**Answer:**  
The `visited` set stores cells that have already been explored. In undirected graphs or mazes with loops, an unvisited neighbor could point back to the current node. Without a `visited` set, the algorithms would cycle infinitely back and forth between adjacent cells, resulting in an infinite loop or memory exhaustion.

#### Q12: How is the final solution path reconstructed after reaching the exit?
**Answer:**  
During the search, we maintain a `parent` dictionary where `parent[child] = current_node`. Once `current_node == exit_pos`, we backtrack from `exit_pos` by following parent pointers until reaching `start_pos` (whose parent is `None`). We then reverse this reconstructed list to obtain the ordered path from Start to Exit.

---

### Section 4: Complexity & Optimality Analysis

#### Q13: What is the time complexity of DFS and BFS on an $R \times C$ maze?
**Answer:**  
Both DFS and BFS have an asymptotic worst-case time complexity of:
$$\mathcal{O}(V + E)$$
Where:
- $V \le R \times C$ (the number of walkable corridor cells).
- $E \le 4V$ (since each cell has at most 4 orthogonal neighbors).  
Since $E = \mathcal{O}(V)$, the total time complexity simplifies to $\mathcal{O}(V) = \mathcal{O}(R \times C)$.

#### Q14: What is the space complexity of DFS and BFS?
**Answer:**  
Both algorithms have an auxiliary space complexity of $\mathcal{O}(V) = \mathcal{O}(R \times C)$:
- **DFS:** Requires $\mathcal{O}(V)$ memory for the recursion/explicit stack and the `visited` set.
- **BFS:** Requires $\mathcal{O}(V)$ memory for the frontier queue and the `visited` set.

#### Q15: Why does BFS guarantee the shortest path in an unweighted maze, while DFS does not?
**Answer:**  
In an unweighted graph, all edge weights are equal ($w = 1$). BFS visits all nodes at distance $k$ strictly before visiting any node at distance $k + 1$. Therefore, the very first time BFS touches the exit cell, it is mathematically impossible for any shorter path to exist.  
DFS, on the other hand, commits to whichever branch it encounters first and continues to the goal without exploring neighboring alternatives. As a result, it returns the *first* path found, which is often suboptimal.

#### Q16: Can DFS ever be faster than BFS in wall-clock time?
**Answer:**  
Yes! If the exit happens to lie directly along the first branch that DFS explores, DFS will reach the exit after visiting only $\mathcal{O}(d)$ nodes (where $d$ is path length), while BFS must systematically explore all surrounding nodes in every direction up to depth $d$.

#### Q17: What are the Best-Case and Worst-Case scenarios for DFS and BFS?
**Answer:**  
- **DFS Best Case:** Goal lies directly along the first branch explored ($\mathcal{O}(d)$ time, $\mathcal{O}(d)$ space).  
- **DFS Worst Case:** Goal lies on the very last branch explored after traversing all dead-ends ($\mathcal{O}(V + E)$ time).  
- **BFS Best Case:** Goal is adjacent to the start node ($\mathcal{O}(1)$ time).  
- **BFS Worst Case:** Goal is at the maximum distance or unreachable ($\mathcal{O}(V + E)$ time and frontier width space).

---

### Section 5: Practical Implementation & Pygame GUI

#### Q18: How does the game maintain a smooth frame rate during algorithm visualization?
**Answer:**  
Instead of freezing the Pygame window with `time.sleep()`, the application records the sequence of visited cells in `explored_order`. In each iteration of the main game loop (`clock.tick(60)`), the application renders a batch of $N$ newly revealed cells (e.g., 4 cells per frame) and refreshes the display. This keeps the event loop 100% responsive to button clicks, player keypresses, and window resizing.

#### Q19: What information does the in-game analytics panel display?
**Answer:**  
The analytics panel displays:
1. Current Game State (`Play Mode`, `Solving DFS`, `Solving BFS`, `Solved`, `Victory`).
2. Live Metrics: Selected Algorithm, Nodes Explored count, Solution Path Length, and CPU Execution Time in milliseconds.
3. Optimality verification (e.g. "GUARANTEED SHORTEST" for BFS).
4. Side-by-side comparative table showing DFS vs BFS metrics on the exact same maze.
5. Map Legend and keyboard shortcut hints.

#### Q20: How are button hover effects and click events implemented?
**Answer:**  
A dedicated `Button` class wraps a `pygame.Rect`. On `pygame.MOUSEMOTION`, `rect.collidepoint(event.pos)` checks if the cursor is hovering over the button to toggle a brighter hover color. On `pygame.MOUSEBUTTONDOWN`, it returns `True` to trigger the associated callback function.

---

### Section 6: Viva Rapid-Fire Questions

#### Q21: What is an unweighted graph?
**Answer:** A graph where all edges have the same uniform cost (in our maze, each step equals 1 move).

#### Q22: What happens if you run Dijkstra's algorithm on an unweighted grid?
**Answer:** When all edge weights are equal to 1, Dijkstra's algorithm behaves identically to Breadth-First Search, but with an unnecessary $\mathcal{O}(\log V)$ priority queue overhead.

#### Q23: What is the Manhattan distance?
**Answer:** The sum of absolute differences of Cartesian coordinates: $D = |x_1 - x_2| + |y_1 - y_2|$. It represents the minimum number of orthogonal grid steps between two cells with no obstacles.

#### Q24: How would you extend this project to A* Search?
**Answer:** By replacing the FIFO queue in BFS with a Min-Priority Queue ordered by $f(n) = g(n) + h(n)$, where $g(n)$ is the exact step cost from the start and $h(n)$ is the Manhattan distance heuristic to the exit.

#### Q25: What is the main conclusion you would present to your examiner?
**Answer:**  
"Through this project, we have empirically proved that while both DFS and BFS share an identical asymptotic time complexity of $\mathcal{O}(V + E)$, their data structure choice fundamentally dictates their behavior. A FIFO queue enables BFS to systematically guarantee the shortest path on unweighted graphs, whereas a LIFO stack causes DFS to explore deep, potentially suboptimal branches."
