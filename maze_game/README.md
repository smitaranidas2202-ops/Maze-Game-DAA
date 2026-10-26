# Maze Game Using Basic DSA Algorithms in Python (DFS vs BFS)

> **College Mini-Project**  
> **Course:** Design and Analysis of Algorithms (DAA)  
> **Target Audience:** Engineering Undergraduates, Faculty Examiners, and Viva Evaluators  
> **Built With:** Python 3, Pygame-ce, Basic Data Structures (2D Arrays, Stacks, Queues)

---

## 1. Project Overview & Objectives

This project is an interactive, educational **Maze Game & Pathfinding Visualizer** written in pure Python using **Pygame**. It bridges theoretical computer science concepts taught in **Design and Analysis of Algorithms (DAA)** with hands-on, real-time graphical visualization.

### Primary Objectives:
1. **Interactive Navigation:** Allow the player to manually navigate through a procedurally generated maze from the Start node to the Exit node using keyboard controls while strictly preventing movement through walls.
2. **Procedural Solvable Mazes:** Generate randomized 2D grid mazes using the **Randomized Depth-First Search (Recursive Backtracker)** algorithm, ensuring that at least one valid path always exists between start and finish.
3. **Core DSA Demonstration:** Implement:
   - **Depth-First Search (DFS)** using an explicit **LIFO Stack**.
   - **Breadth-First Search (BFS)** using a **FIFO Queue**.
4. **Algorithmic Benchmarking & Shortest Path Verification:** Provide empirical, side-by-side comparisons of **Nodes Explored**, **Path Length**, and **Execution Time (ms)** to demonstrate why BFS guarantees the shortest path on unweighted graphs while DFS does not.

---

## 2. Visual Demonstration

| Initial Play Mode | DFS Traversal (Stack / LIFO) | BFS Traversal (Queue / FIFO) | Victory Screen |
| :---: | :---: | :---: | :---: |
| ![Play Mode](screenshot_play_mode.png) | ![DFS Solved](screenshot_dfs_solved.png) | ![BFS Solved](screenshot_bfs_solved.png) | ![Victory](screenshot_victory.png) |

---

## 3. Technology Stack & Data Structures

- **Programming Language:** Python 3.10+ (tested on Python 3.11, 3.12, 3.13, 3.14)
- **GUI & Graphics Framework:** Pygame / Pygame-ce
- **Data Structures Utilized:**
  1. **2D Array (`list` of `lists`):** Represents the maze matrix `grid[row][col]`.
  2. **Stack (LIFO):** Powers the DFS solver and procedural maze generation.
  3. **Queue (FIFO - `collections.deque`):** Powers the BFS shortest-path solver.
  4. **Hash Set (`set`):** $O(1)$ visited lookup table to prevent infinite loops.
  5. **Hash Map (`dict`):** Parent lookup dictionary `parent[child] = curr` for linear path reconstruction.

---

## 4. Project Directory Structure

```text
maze_game/
├── main.py                     # Main Pygame application, game loop, UI rendering, event handling
├── maze.py                     # 2D grid representation, wall collisions, randomized maze generation
├── algorithms.py               # Depth-First Search (DFS) & Breadth-First Search (BFS) implementations
├── requirements.txt            # Python dependencies (pygame-ce, pytest)
├── test_maze_game.py           # 7 automated unit & integration test cases
├── PROJECT_REPORT.md           # Formal college mini-project academic report
├── VIVA_QUESTIONS_AND_ANSWERS.md # 25+ viva questions with in-depth technical explanations
├── screenshot_play_mode.png    # Demonstration screenshot: Player mode
├── screenshot_dfs_solved.png   # Demonstration screenshot: DFS animated solution
├── screenshot_bfs_solved.png   # Demonstration screenshot: BFS shortest path solution
├── screenshot_victory.png      # Demonstration screenshot: Player victory modal
└── README.md                   # This project guide and technical documentation
```

---

## 5. Installation & Execution Guide

### Prerequisites
Make sure Python 3.10 or higher is installed on your computer.

### Step 1: Clone or Navigate to the Project Directory
```bash
cd "maze_game"
```

### Step 2: Create and Activate a Virtual Environment (Recommended)
```bash
# On macOS / Linux:
python3 -m venv venv
source venv/bin/activate

# On Windows:
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Required Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Interactive Game
```bash
python main.py
```
*(Or from the project root workspace directory, run `python run_maze_game.py` or `python run.py`)*

### Step 5: Run Automated Tests
```bash
python -m pytest test_maze_game.py -v
```
*(Or `python test_maze_game.py`)*

---

## 6. Game Controls & UI Guide

### Manual Player Movement
- **Move Up:** `W` or `Up Arrow`
- **Move Down:** `S` or `Down Arrow`
- **Move Left:** `A` or `Left Arrow`
- **Move Right:** `D` or `Right Arrow`

### Quick Keyboard Shortcuts
| Shortcut | Action | Description |
| :--- | :--- | :--- |
| `P` | **Play Mode** | Takes manual control of the player avatar |
| `G` | **Generate Maze** | Creates a new procedurally generated solvable maze |
| `1` or `D` | **Solve Using DFS** | Animates Depth-First Search exploration and path |
| `2` or `B` | **Solve Using BFS** | Animates Breadth-First Search exploration and shortest path |
| `R` | **Reset Position** | Teleports player back to Start and clears solver overlay |
| `Space` | **Instant Solve** | Skips animation to immediately view the solution |
| `Esc` | **Quit Game** | Exits the application |

### Screen Map Legend
- **Green Cell (`S`):** Starting point at coordinates `(1, 1)`.
- **Red Cell (`E`):** Exit destination at coordinates `(rows - 2, cols - 2)`.
- **Sky Blue Circle:** Player character.
- **Dark Navy Slate:** Solid impassable walls (`WALL = 1`).
- **Clean Soft White:** Walkable corridor pathways (`PATH = 0`).
- **Warm Peach Cells:** Cells explored by DFS during stack-based search.
- **Ice Cyan Cells:** Cells explored by BFS during queue-based search.
- **Purple / Violet Line:** Final reconstructed solution path from Start to Exit.

---

## 7. Design and Analysis of Algorithms (DAA) Theoretical Deep Dive

### 7.1 Representation of the Maze as a 2D Array
The maze is modeled as a discrete 2D matrix (unweighted orthogonal grid graph $G = (V, E)$):
$$\text{grid}[r][c] \in \{0, 1\}$$
- **Vertices ($V$):** Every open cell where `grid[r][c] == 0` corresponds to a graph vertex $v \in V$.
- **Edges ($E$):** For any two open cells $(r_1, c_1)$ and $(r_2, c_2)$ sharing a common boundary ($|r_1 - r_2| + |c_1 - c_2| = 1$), an undirected unweighted edge of weight $w = 1$ exists between them.
- **Boundary Guarantee:** Outer perimeter rows ($r = 0$, $r = R-1$) and columns ($c = 0$, $c = C-1$) are initialized as solid walls, preventing off-grid indexing.

---

### 7.2 Stacks vs Queues: Impact on Search Traversal

```text
       DFS (Stack / LIFO)                        BFS (Queue / FIFO)
  
       +---------------+                         +---------------+
PUSH ->| Node C (Top)  | -> POP          ENQUEUE | Node C Node B | -> DEQUEUE
       | Node B        |                         +---------------+
       | Node A        |                                 ^
       +---------------+                           (Level Order)
         (Dives Deep)
```

1. **Depth-First Search (DFS) with a LIFO Stack:**
   - In DFS, the most recently discovered neighbor is pushed to the top of the stack and popped first on the subsequent iteration.
   - **Behavior:** DFS greedily plunges deep down a single corridor until it hits a dead end (leaf node), at which point it backtracks to explore remaining branches.
   - **Result:** DFS can take long, convoluted detours and is **NOT guaranteed** to find the shortest path.

2. **Breadth-First Search (BFS) with a FIFO Queue:**
   - In BFS, newly discovered neighbors are enqueued at the back of the queue, while nodes are processed from the front.
   - **Behavior:** BFS expands uniformly in expanding concentric circles (level by level), visiting all cells at distance $k$ before visiting any cell at distance $k + 1$.
   - **Result:** The first time the exit node is reached, it is mathematically guaranteed to be via the minimum number of steps. Hence, BFS is **optimal for unweighted graphs**.

---

### 7.3 Complexity Analysis Table

Let $V \le R \times C$ be the number of walkable cells (vertices) and $E \le 4V$ be the number of walkable orthogonal connections (edges).

| Metric | Depth-First Search (DFS) | Breadth-First Search (BFS) |
| :--- | :--- | :--- |
| **Data Structure** | **Stack** (LIFO: `list.append()`, `list.pop()`) | **Queue** (FIFO: `deque.append()`, `deque.popleft()`) |
| **Traversal Style** | Deep branch exploration with backtracking | Level-by-level concentric expansion |
| **Time Complexity (Worst Case)** | $\mathcal{O}(V + E) = \mathcal{O}(R \times C)$ | $\mathcal{O}(V + E) = \mathcal{O}(R \times C)$ |
| **Time Complexity (Best Case)** | $\mathcal{O}(d)$ (where exit lies on the first chosen branch) | $\mathcal{O}(b^d)$ (where $d$ is depth to goal) |
| **Space Complexity (Auxiliary)** | $\mathcal{O}(V)$ for the recursion/explicit stack | $\mathcal{O}(V)$ for the frontier queue |
| **Shortest Path Guarantee?** | ❌ **No** (often returns sub-optimal paths) | ✅ **Yes** (strictly optimal on unweighted grids) |
| **Complete? (Finds path if exists)** | ✅ Yes (on finite graphs) | ✅ Yes |

---

### 7.4 Why BFS Finds the Shortest Path in Unweighted Mazes

In an unweighted grid, every step from one cell to an adjacent cell has an identical cost of $w(u, v) = 1$.

**Formal Invariant:**  
At any point during the execution of BFS, the queue contains vertices whose shortest-path distance from the start node $s$ is either $d$ or $d + 1$. Vertices with distance $d$ are always dequeued strictly before vertices with distance $d + 1$.

**Proof by Contradiction:**  
Suppose BFS discovers the destination node $E$ along path $P_1$ with length $L_1$, but there exists a shorter path $P_2$ with length $L_2 < L_1$.  
Because BFS visits all nodes at distance $L_2$ before any node at distance $L_1$, the node $E$ must have been reached during the processing of level $L_2$. This contradicts the assumption that $P_1$ was the first path discovered. Therefore, the first path found by BFS is guaranteed to have the minimum path length.

---

### 7.5 Empirical Benchmark Comparison (Actual Run Data)

Run on a standard $21 \times 21$ generated maze with braid factor 0.10:

```text
+---------------------+-------------------------+-------------------------+
| Metric              | Depth-First Search (DFS)| Breadth-First Search (BFS)|
+---------------------+-------------------------+-------------------------+
| Data Structure      | Explicit LIFO Stack     | Circular FIFO Queue     |
| Nodes Explored      | 84 cells                | 126 cells               |
| Solution Path Length| 72 steps                | 48 steps (Shortest!)    |
| CPU Execution Time  | 0.065 ms                | 0.089 ms                |
| Optimality          | Sub-optimal detour      | Mathematically Optimal  |
+---------------------+-------------------------+-------------------------+
```

> **Key Viva Observation:** Notice how BFS explored slightly more nodes (126 vs 84) because it searched radially in all directions, but in return it discovered a solution path that was **33% shorter (48 vs 72 steps)** than the path discovered by DFS!

---

## 8. College Viva Questions & Quick Answers

1. **Q: Why are odd dimensions (e.g. $21 \times 21$) used for the maze grid?**  
   *A:* In grid-based maze carving algorithms like Recursive Backtracker, cells at odd row and column indices act as path chambers, while cells at even coordinates act as dividing walls. Odd grid dimensions ensure a clean boundary of solid perimeter walls surrounding the maze.

2. **Q: How does path reconstruction work after the algorithm reaches the exit?**  
   *A:* During traversal, we record each neighbor's predecessor in a `parent` dictionary (`parent[neighbor] = current`). Once the exit is reached, we trace backwards from `exit` to `parent[exit]` until reaching `None` (the start node), and reverse the resulting list.

3. **Q: What is "braiding" in maze generation, and why is it important for DAA?**  
   *A:* A perfect tree maze has zero cycles, meaning there is only one unique path between start and exit. Braiding removes a small percentage of dead-end walls to introduce loops/cycles. This creates multiple alternate paths, allowing us to vividly demonstrate how BFS finds the shorter path while DFS may take a longer detour.

*(For the complete bank of 25+ viva questions and model answers, refer to [VIVA_QUESTIONS_AND_ANSWERS.md](file:///Users/rohanughade/Desktop/Ideathon%20Project/maze_game/VIVA_QUESTIONS_AND_ANSWERS.md))*

---

## 9. License & Academic Attribution
Developed as an educational mini-project for **Design and Analysis of Algorithms (DAA)**. Free for academic, classroom, and demonstrative learning purposes.
## Game Screenshots

### Gameplay
![Maze Game Gameplay](screenshot_play_mode.png)

### BFS Shortest Path
![BFS Solved Maze](screenshot_bfs_solved.png)

### DFS Traversal
![DFS Solved Maze](screenshot_dfs_solved.png)

### Victory Screen
![Maze Game Victory](screenshot_victory.png)
