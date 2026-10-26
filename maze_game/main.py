"""
main.py - Main Application, Game Loop, and Pygame User Interface
Part of the DAA College Mini-Project: Maze Game Using Basic DSA Algorithms.

This module provides a complete, modern graphical interface for:
- Playing the maze game using Arrow Keys or WASD.
- Generating new random solvable mazes.
- Running and animating Depth-First Search (DFS) and Breadth-First Search (BFS).
- Real-time performance benchmarking (nodes explored, path length, execution time).
- In-game side-by-side comparison table demonstrating why BFS finds the shortest path.
"""

import sys
import os
import pygame

# Ensure current directory is on sys.path for local module imports
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from maze import Maze, PATH, WALL
from algorithms import solve_dfs, solve_bfs, SearchResult


# ---------------------------------------------------------------------------
# COLOR PALETTE (Modern high-contrast theme)
# ---------------------------------------------------------------------------
COLOR_BG            = (15, 23, 42)      # Deep Navy Slate (#0F172A)
COLOR_PANEL_BG      = (30, 41, 59)      # Dark Slate (#1E293B)
COLOR_CARD_BG       = (51, 65, 85)      # Slate Card (#334155)
COLOR_CARD_BORDER   = (71, 85, 105)     # Slate Border (#475569)

# Maze Colors
COLOR_WALL          = (15, 23, 42)      # Wall cell (#0F172A)
COLOR_PATH          = (248, 250, 252)   # Walkable path cell (#F8FAFC)
COLOR_START         = (34, 197, 94)     # Start node: Emerald Green (#22C55E)
COLOR_EXIT          = (239, 68, 68)     # Exit node: Coral Red (#EF4444)
COLOR_PLAYER        = (14, 165, 233)    # Player token: Sky Blue (#0EA5E9)
COLOR_PLAYER_TRAIL  = (186, 230, 253)   # Soft blue trail for player

# Algorithm Visualization Colors
COLOR_EXPLORED_DFS  = (254, 215, 170)   # DFS Explored: Warm Peach (#FED7AA)
COLOR_EXPLORED_BFS  = (186, 230, 253)   # BFS Explored: Soft Ice Cyan (#BAE6FD)
COLOR_SOLUTION_PATH = (168, 85, 247)    # Final Reconstructed Path: Violet (#A855F7)
COLOR_PATH_START    = (74, 222, 128)    # Path Start highlight

# UI Text & Buttons
COLOR_TEXT_WHITE    = (255, 255, 255)
COLOR_TEXT_MUTED    = (148, 163, 184)   # Slate 400
COLOR_TEXT_ACCENT   = (56, 189, 248)    # Cyan 400
COLOR_SUCCESS       = (74, 222, 128)    # Green 400
COLOR_WARNING       = (251, 191, 36)    # Amber 400

# Button Colors
COLOR_BTN_NORMAL    = (59, 130, 246)    # Vibrant Blue
COLOR_BTN_HOVER     = (96, 165, 250)
COLOR_BTN_TEXT      = (255, 255, 255)
COLOR_BTN_DFS       = (249, 115, 22)    # Orange for DFS
COLOR_BTN_DFS_HOV   = (251, 146, 60)
COLOR_BTN_BFS       = (6, 182, 212)     # Cyan for BFS
COLOR_BTN_BFS_HOV   = (34, 211, 238)
COLOR_BTN_RESET     = (100, 116, 139)   # Slate for Reset
COLOR_BTN_RESET_HOV = (148, 163, 184)


# ---------------------------------------------------------------------------
# GAME STATE CONSTANTS
# ---------------------------------------------------------------------------
MODE_PLAY        = "PLAY"          # Manual player navigation
MODE_SOLVING_DFS = "SOLVING_DFS"   # Animating DFS exploration
MODE_SOLVING_BFS = "SOLVING_BFS"   # Animating BFS exploration
MODE_SOLVED      = "SOLVED"        # Algorithm finished, solution displayed
MODE_VICTORY     = "VICTORY"       # Player reached the exit!


def get_font(size, bold=False):
    """
    Safely load a cross-platform font without triggering OS font directory
    permission errors on macOS or Linux.
    """
    try:
        font = pygame.font.Font(None, size)
        font.set_bold(bold)
        return font
    except Exception:
        return pygame.font.Font(None, size)


# ---------------------------------------------------------------------------
# BUTTON COMPONENT CLASS
# ---------------------------------------------------------------------------
class Button:
    """
    Interactive UI Button with hover feedback and click callbacks.
    """

    def __init__(self, rect, text, bg_color=COLOR_BTN_NORMAL, hover_color=COLOR_BTN_HOVER, text_color=COLOR_BTN_TEXT):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False

    def handle_event(self, event):
        """Update hover state and return True if clicked."""
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

    def draw(self, surface, font):
        """Render the rounded button."""
        color = self.hover_color if self.is_hovered else self.bg_color
        # Draw soft shadow
        shadow_rect = self.rect.copy()
        shadow_rect.y += 2
        pygame.draw.rect(surface, (10, 15, 28), shadow_rect, border_radius=6)
        # Draw main button
        pygame.draw.rect(surface, color, self.rect, border_radius=6)
        # Draw text
        txt_surf = font.render(self.text, True, self.text_color)
        txt_rect = txt_surf.get_rect(center=self.rect.center)
        surface.blit(txt_surf, txt_rect)


# ---------------------------------------------------------------------------
# MAIN GAME APPLICATION CLASS
# ---------------------------------------------------------------------------
class MazeGameApp:
    """
    Main application managing the game window, event loop, state transitions,
    rendering, and algorithm visualization.
    """

    def __init__(self, screen_width=1040, screen_height=700, maze_size=21):
        pygame.init()
        pygame.display.set_caption("Maze Game - DAA Algorithms Mini-Project (DFS vs BFS)")

        self.width = screen_width
        self.height = screen_height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

        # Fonts (Cross-platform and permission-safe)
        self.font_title = get_font(26, bold=True)
        self.font_subtitle = get_font(15)
        self.font_header = get_font(17, bold=True)
        self.font_body = get_font(15)
        self.font_bold = get_font(15, bold=True)
        self.font_btn = get_font(15, bold=True)
        self.font_mini = get_font(13)

        # Maze parameters
        self.maze_size = maze_size
        self.maze = Maze(rows=self.maze_size, cols=self.maze_size, braid_prob=0.10)

        # Maze rendering area (left side)
        self.maze_offset_x = 24
        self.maze_offset_y = 68
        self.maze_display_size = 600
        self.cell_size = self.maze_display_size // self.maze.rows

        # Player state
        self.player_pos = list(self.maze.start_pos)
        self.player_moves = 0
        self.player_trail = [tuple(self.player_pos)]

        # Algorithm solver state
        self.current_result = None
        self.dfs_result = None
        self.bfs_result = None
        self.explored_cells_drawn = []
        self.solution_path_drawn = []
        self.animation_step = 0
        self.path_animation_step = 0
        self.animation_speed = 4  # Cells explored per frame

        # Application state
        self.mode = MODE_PLAY
        self.status_message = "Play Mode: Use Arrow Keys or WASD to reach Exit (Red)."

        # Initialize interactive buttons
        self._init_buttons()

    def _init_buttons(self):
        """Create buttons for the right-hand control panel."""
        panel_x = 652
        btn_w = 175
        btn_h = 34
        start_y = 110
        spacing = 42

        self.btn_play = Button(
            (panel_x, start_y, btn_w, btn_h),
            "Play Mode (WASD)",
            bg_color=(37, 99, 235),
            hover_color=(59, 130, 246)
        )
        self.btn_new_maze = Button(
            (panel_x + btn_w + 12, start_y, btn_w, btn_h),
            "New Random Maze",
            bg_color=(13, 148, 136),
            hover_color=(20, 184, 166)
        )
        self.btn_dfs = Button(
            (panel_x, start_y + spacing, btn_w, btn_h),
            "Solve Using DFS",
            bg_color=COLOR_BTN_DFS,
            hover_color=COLOR_BTN_DFS_HOV
        )
        self.btn_bfs = Button(
            (panel_x + btn_w + 12, start_y + spacing, btn_w, btn_h),
            "Solve Using BFS",
            bg_color=COLOR_BTN_BFS,
            hover_color=COLOR_BTN_BFS_HOV
        )
        self.btn_reset = Button(
            (panel_x, start_y + spacing * 2, btn_w, btn_h),
            "Reset Position",
            bg_color=COLOR_BTN_RESET,
            hover_color=COLOR_BTN_RESET_HOV
        )
        self.btn_instant = Button(
            (panel_x + btn_w + 12, start_y + spacing * 2, btn_w, btn_h),
            "Instant / Skip Anim",
            bg_color=(109, 40, 217),
            hover_color=(124, 58, 237)
        )

        self.buttons = [
            self.btn_play,
            self.btn_new_maze,
            self.btn_dfs,
            self.btn_bfs,
            self.btn_reset,
            self.btn_instant
        ]

    def reset_player(self):
        """Reset the player back to the maze start position."""
        self.player_pos = list(self.maze.start_pos)
        self.player_moves = 0
        self.player_trail = [tuple(self.player_pos)]
        self.current_result = None
        self.explored_cells_drawn = []
        self.solution_path_drawn = []
        self.animation_step = 0
        self.path_animation_step = 0
        self.mode = MODE_PLAY
        self.status_message = "Reset complete. Ready to play with WASD or Arrow Keys!"

    def new_maze(self):
        """Generate a brand-new random solvable maze."""
        self.maze.generate()
        self.dfs_result = None
        self.bfs_result = None
        self.reset_player()
        self.status_message = "New random solvable maze generated successfully!"

    def start_dfs_solver(self):
        """Run Depth-First Search and prepare animation."""
        self.mode = MODE_SOLVING_DFS
        self.explored_cells_drawn = []
        self.solution_path_drawn = []
        self.animation_step = 0
        self.path_animation_step = 0

        # Execute DFS algorithm on the current maze
        self.current_result = solve_dfs(self.maze)
        self.dfs_result = self.current_result
        self.status_message = "Running DFS (Stack/LIFO)... Exploring deep branches."

    def start_bfs_solver(self):
        """Run Breadth-First Search and prepare animation."""
        self.mode = MODE_SOLVING_BFS
        self.explored_cells_drawn = []
        self.solution_path_drawn = []
        self.animation_step = 0
        self.path_animation_step = 0

        # Execute BFS algorithm on the current maze
        self.current_result = solve_bfs(self.maze)
        self.bfs_result = self.current_result
        self.status_message = "Running BFS (Queue/FIFO)... Expanding in concentric rings."

    def instant_complete_solver(self):
        """Instantly finish the currently running or last selected solver."""
        if self.current_result is None:
            # Run BFS by default if nothing was run yet
            self.start_bfs_solver()

        self.explored_cells_drawn = list(self.current_result.explored_order)
        self.solution_path_drawn = list(self.current_result.path)
        self.mode = MODE_SOLVED
        self.status_message = f"Solved via {self.current_result.algorithm_name}! Path: {self.current_result.path_length} steps."

    def handle_player_move(self, dr, dc):
        """
        Handle manual movement for the player token.
        Prevents moving through walls and checks for victory.
        """
        if self.mode != MODE_PLAY and self.mode != MODE_VICTORY:
            # Switch back to play mode on movement key
            self.mode = MODE_PLAY

        new_r = self.player_pos[0] + dr
        new_c = self.player_pos[1] + dc

        # Check bounds and wall collision
        if self.maze.is_valid_move(new_r, new_c):
            self.player_pos = [new_r, new_c]
            self.player_moves += 1
            if (new_r, new_c) not in self.player_trail:
                self.player_trail.append((new_r, new_c))

            # Check for victory
            if tuple(self.player_pos) == self.maze.exit_pos:
                self.mode = MODE_VICTORY
                self.status_message = f"VICTORY! You solved the maze in {self.player_moves} moves! Press R to replay or G for new maze."
            else:
                self.status_message = f"Moving: Step {self.player_moves}. Navigate towards Exit (Red)."

    def update_animation(self):
        """Advance the solver visualization step-by-step."""
        if self.mode in (MODE_SOLVING_DFS, MODE_SOLVING_BFS) and self.current_result:
            explored = self.current_result.explored_order

            # Animate explored nodes first
            if self.animation_step < len(explored):
                end_idx = min(self.animation_step + self.animation_speed, len(explored))
                self.explored_cells_drawn = explored[:end_idx]
                self.animation_step = end_idx
            else:
                # Once exploration is complete, animate the solution path
                path = self.current_result.path
                if self.path_animation_step < len(path):
                    path_end = min(self.path_animation_step + 2, len(path))
                    self.solution_path_drawn = path[:path_end]
                    self.path_animation_step = path_end
                else:
                    self.mode = MODE_SOLVED
                    opt_text = "GUARANTEED SHORTEST" if self.current_result.is_optimal else "EXPLORATORY (Not Guaranteed Shortest)"
                    self.status_message = (
                        f"Search Finished! Explored {self.current_result.nodes_explored} nodes. "
                        f"Path length: {self.current_result.path_length} steps ({opt_text})."
                    )

    def draw_top_bar(self):
        """Draw application title and top banner."""
        # Main title
        title_surf = self.font_title.render("Maze Game & Pathfinding Visualizer", True, COLOR_TEXT_WHITE)
        self.screen.blit(title_surf, (24, 14))

        # College / DAA Subject badge
        tag_surf = self.font_bold.render(" DAA MINI-PROJECT ", True, (15, 23, 42))
        tag_bg = pygame.Rect(440, 16, tag_surf.get_width() + 10, 24)
        pygame.draw.rect(self.screen, (56, 189, 248), tag_bg, border_radius=4)
        self.screen.blit(tag_surf, (tag_bg.x + 5, tag_bg.y + 3))

        sub_surf = self.font_subtitle.render("Comparative Study of Depth-First Search (DFS) vs Breadth-First Search (BFS)", True, COLOR_TEXT_MUTED)
        self.screen.blit(sub_surf, (24, 42))

        # Status notification line
        status_bg = pygame.Rect(24, self.height - 30, self.maze_display_size, 22)
        pygame.draw.rect(self.screen, (20, 29, 47), status_bg, border_radius=4)
        status_surf = self.font_body.render(self.status_message, True, COLOR_WARNING if self.mode == MODE_VICTORY else COLOR_TEXT_WHITE)
        self.screen.blit(status_surf, (30, self.height - 28))

    def draw_maze(self):
        """Render the 2D maze grid with walls, paths, explored cells, and player."""
        # Background frame for maze
        frame_rect = pygame.Rect(
            self.maze_offset_x - 4,
            self.maze_offset_y - 4,
            self.cell_size * self.maze.cols + 8,
            self.cell_size * self.maze.rows + 8
        )
        pygame.draw.rect(self.screen, COLOR_CARD_BORDER, frame_rect, width=2, border_radius=6)

        explored_set = set(self.explored_cells_drawn)
        path_set = set(self.solution_path_drawn)
        trail_set = set(self.player_trail)

        # Draw each cell
        for r in range(self.maze.rows):
            for c in range(self.maze.cols):
                cell_rect = pygame.Rect(
                    self.maze_offset_x + c * self.cell_size,
                    self.maze_offset_y + r * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )

                if self.maze.grid[r][c] == WALL:
                    # Wall cell
                    pygame.draw.rect(self.screen, COLOR_WALL, cell_rect)
                else:
                    # Default walkable path
                    cell_color = COLOR_PATH

                    # Explored coloring
                    if (r, c) in explored_set:
                        if self.current_result and "DFS" in self.current_result.algorithm_name:
                            cell_color = COLOR_EXPLORED_DFS
                        else:
                            cell_color = COLOR_EXPLORED_BFS

                    # Player manual path trail
                    elif self.mode in (MODE_PLAY, MODE_VICTORY) and (r, c) in trail_set:
                        cell_color = COLOR_PLAYER_TRAIL

                    # Solution path coloring (overrides explored)
                    if (r, c) in path_set:
                        cell_color = COLOR_SOLUTION_PATH

                    # Special Start and Exit coloring
                    if (r, c) == self.maze.start_pos:
                        cell_color = COLOR_START
                    elif (r, c) == self.maze.exit_pos:
                        cell_color = COLOR_EXIT

                    pygame.draw.rect(self.screen, cell_color, cell_rect)

                    # Subtle inner grid line
                    pygame.draw.rect(self.screen, (226, 232, 240), cell_rect, width=1)

                    # Label Start 'S' and Exit 'E'
                    if (r, c) == self.maze.start_pos:
                        s_text = self.font_bold.render("S", True, (255, 255, 255))
                        self.screen.blit(s_text, s_text.get_rect(center=cell_rect.center))
                    elif (r, c) == self.maze.exit_pos:
                        e_text = self.font_bold.render("E", True, (255, 255, 255))
                        self.screen.blit(e_text, e_text.get_rect(center=cell_rect.center))

        # Draw Player Token (in Play Mode or idle)
        player_r, player_c = self.player_pos
        player_rect = pygame.Rect(
            self.maze_offset_x + player_c * self.cell_size,
            self.maze_offset_y + player_r * self.cell_size,
            self.cell_size,
            self.cell_size
        )
        # Player outer ring & inner circle
        center = player_rect.center
        radius = max(3, self.cell_size // 2 - 3)
        pygame.draw.circle(self.screen, (30, 64, 175), center, radius + 2)
        pygame.draw.circle(self.screen, COLOR_PLAYER, center, radius)
        pygame.draw.circle(self.screen, (255, 255, 255), center, max(1, radius // 2))

    def draw_side_panel(self):
        """Render controls, legend, analytics, and comparison table."""
        panel_x = 648
        panel_y = 64
        panel_w = 370
        panel_h = self.height - 80

        # Background container
        panel_rect = pygame.Rect(panel_x, panel_y, panel_w, panel_h)
        pygame.draw.rect(self.screen, COLOR_PANEL_BG, panel_rect, border_radius=8)
        pygame.draw.rect(self.screen, COLOR_CARD_BORDER, panel_rect, width=1, border_radius=8)

        # Panel Section 1: Mode & Control Buttons
        sec1_title = self.font_header.render("CONTROL PANEL", True, COLOR_TEXT_ACCENT)
        self.screen.blit(sec1_title, (panel_x + 14, panel_y + 12))

        # Current State Badge
        mode_colors = {
            MODE_PLAY: ((37, 99, 235), "PLAY MODE (Player Active)"),
            MODE_SOLVING_DFS: (COLOR_BTN_DFS, "ANIMATING: DFS SOLVER"),
            MODE_SOLVING_BFS: (COLOR_BTN_BFS, "ANIMATING: BFS SOLVER"),
            MODE_SOLVED: ((147, 51, 234), "MAZE SOLVED"),
            MODE_VICTORY: (COLOR_SUCCESS, "🎉 VICTORY! EXIT REACHED")
        }
        badge_color, badge_text = mode_colors.get(self.mode, (COLOR_BTN_NORMAL, self.mode))
        badge_surf = self.font_bold.render(f"  {badge_text}  ", True, (255, 255, 255))
        badge_rect = pygame.Rect(panel_x + 155, panel_y + 10, badge_surf.get_width() + 4, 22)
        pygame.draw.rect(self.screen, badge_color, badge_rect, border_radius=4)
        self.screen.blit(badge_surf, (badge_rect.x + 2, badge_rect.y + 2))

        # Draw buttons
        for btn in self.buttons:
            btn.draw(self.screen, self.font_btn)

        # Panel Section 2: Algorithm Performance Card
        card_y = panel_y + 180
        card_w = panel_w - 24
        card_h = 168
        card_rect = pygame.Rect(panel_x + 12, card_y, card_w, card_h)
        pygame.draw.rect(self.screen, COLOR_CARD_BG, card_rect, border_radius=6)
        pygame.draw.rect(self.screen, COLOR_CARD_BORDER, card_rect, width=1, border_radius=6)

        card_title = self.font_header.render("LIVE ALGORITHM METRICS", True, COLOR_TEXT_ACCENT)
        self.screen.blit(card_title, (card_rect.x + 12, card_rect.y + 10))

        if self.current_result:
            r = self.current_result
            metrics = [
                ("Algorithm:", f"{r.algorithm_name}"),
                ("Nodes Explored:", f"{r.nodes_explored} cells ({len(self.explored_cells_drawn)} rendered)"),
                ("Solution Path:", f"{r.path_length} steps"),
                ("Execution Time:", f"{r.execution_time_ms:.3f} ms"),
                ("Optimality:", "GUARANTEED SHORTEST (BFS)" if r.is_optimal else "Sub-optimal / Exploratory (DFS)")
            ]
            for i, (label, val) in enumerate(metrics):
                lbl_surf = self.font_body.render(label, True, COLOR_TEXT_MUTED)
                val_color = COLOR_SUCCESS if ("GUARANTEED" in val or "0." in val) else COLOR_TEXT_WHITE
                val_surf = self.font_bold.render(val, True, val_color)
                line_y = card_rect.y + 36 + i * 24
                self.screen.blit(lbl_surf, (card_rect.x + 12, line_y))
                self.screen.blit(val_surf, (card_rect.x + 126, line_y))
        else:
            p_moves = self.font_body.render(f"Player Current Moves: {self.player_moves}", True, COLOR_TEXT_WHITE)
            p_hint = self.font_body.render("Click 'Solve Using DFS' or 'Solve Using BFS'", True, COLOR_TEXT_MUTED)
            p_hint2 = self.font_body.render("to inspect algorithmic traversal and execution time.", True, COLOR_TEXT_MUTED)
            self.screen.blit(p_moves, (card_rect.x + 12, card_rect.y + 40))
            self.screen.blit(p_hint, (card_rect.x + 12, card_rect.y + 70))
            self.screen.blit(p_hint2, (card_rect.x + 12, card_rect.y + 94))

        # Panel Section 3: Comparative Table (DFS vs BFS)
        table_y = card_y + card_h + 12
        table_h = 135
        table_rect = pygame.Rect(panel_x + 12, table_y, card_w, table_h)
        pygame.draw.rect(self.screen, COLOR_CARD_BG, table_rect, border_radius=6)
        pygame.draw.rect(self.screen, COLOR_CARD_BORDER, table_rect, width=1, border_radius=6)

        t_title = self.font_header.render("DFS vs BFS COMPARISON TABLE", True, COLOR_TEXT_ACCENT)
        self.screen.blit(t_title, (table_rect.x + 12, table_rect.y + 8))

        # Table Headers
        col_metric = table_rect.x + 12
        col_dfs = table_rect.x + 165
        col_bfs = table_rect.x + 258

        h_metric = self.font_bold.render("Metric", True, COLOR_TEXT_MUTED)
        h_dfs = self.font_bold.render("DFS (Stack)", True, (251, 146, 60))
        h_bfs = self.font_bold.render("BFS (Queue)", True, (34, 211, 238))

        self.screen.blit(h_metric, (col_metric, table_rect.y + 30))
        self.screen.blit(h_dfs, (col_dfs, table_rect.y + 30))
        self.screen.blit(h_bfs, (col_bfs, table_rect.y + 30))

        # Horizontal separator
        pygame.draw.line(self.screen, COLOR_CARD_BORDER, (table_rect.x + 8, table_rect.y + 48), (table_rect.x + card_w - 8, table_rect.y + 48))

        # Populate rows
        dfs_exp = f"{self.dfs_result.nodes_explored}" if self.dfs_result else "-"
        bfs_exp = f"{self.bfs_result.nodes_explored}" if self.bfs_result else "-"
        dfs_len = f"{self.dfs_result.path_length}" if self.dfs_result else "-"
        bfs_len = f"{self.bfs_result.path_length}" if self.bfs_result else "-"
        dfs_time = f"{self.dfs_result.execution_time_ms:.2f} ms" if self.dfs_result else "-"
        bfs_time = f"{self.bfs_result.execution_time_ms:.2f} ms" if self.bfs_result else "-"

        table_rows = [
            ("Explored Nodes", dfs_exp, bfs_exp),
            ("Path Length", dfs_len, f"{bfs_len} (Shortest)" if self.bfs_result else "-"),
            ("Exec Time (ms)", dfs_time, bfs_time),
        ]

        for i, (m_lbl, d_val, b_val) in enumerate(table_rows):
            row_y = table_rect.y + 54 + i * 20
            self.screen.blit(self.font_mini.render(m_lbl, True, COLOR_TEXT_MUTED), (col_metric, row_y))
            self.screen.blit(self.font_mini.render(d_val, True, COLOR_TEXT_WHITE), (col_dfs, row_y))
            # Highlight BFS shortest path in green
            b_color = COLOR_SUCCESS if "Shortest" in b_val else COLOR_TEXT_WHITE
            self.screen.blit(self.font_mini.render(b_val, True, b_color), (col_bfs, row_y))

        # Explanatory DAA footnote
        note_y = table_rect.y + 114
        note_surf = self.font_mini.render("* BFS guarantees shortest path in unweighted graphs.", True, (148, 163, 184))
        self.screen.blit(note_surf, (col_metric, note_y))

        # Panel Section 4: Color Legend
        legend_y = table_y + table_h + 10
        legend_h = 75
        legend_rect = pygame.Rect(panel_x + 12, legend_y, card_w, legend_h)
        pygame.draw.rect(self.screen, COLOR_CARD_BG, legend_rect, border_radius=6)
        pygame.draw.rect(self.screen, COLOR_CARD_BORDER, legend_rect, width=1, border_radius=6)

        leg_title = self.font_header.render("MAP LEGEND", True, COLOR_TEXT_ACCENT)
        self.screen.blit(leg_title, (legend_rect.x + 12, legend_rect.y + 6))

        # Legend items: (Color, Label, x, y)
        items = [
            (COLOR_START, "Start (S)", legend_rect.x + 12, legend_rect.y + 28),
            (COLOR_EXIT, "Exit (E)", legend_rect.x + 125, legend_rect.y + 28),
            (COLOR_PLAYER, "Player", legend_rect.x + 235, legend_rect.y + 28),
            (COLOR_EXPLORED_DFS, "DFS Visited", legend_rect.x + 12, legend_rect.y + 50),
            (COLOR_EXPLORED_BFS, "BFS Visited", legend_rect.x + 125, legend_rect.y + 50),
            (COLOR_SOLUTION_PATH, "Solution Path", legend_rect.x + 235, legend_rect.y + 50),
        ]
        for color, label, lx, ly in items:
            box = pygame.Rect(lx, ly, 14, 14)
            pygame.draw.rect(self.screen, color, box, border_radius=3)
            pygame.draw.rect(self.screen, (255, 255, 255), box, width=1, border_radius=3)
            lbl = self.font_mini.render(label, True, COLOR_TEXT_WHITE)
            self.screen.blit(lbl, (lx + 18, ly))

    def draw_victory_overlay(self):
        """Draw an celebratory overlay modal when the player reaches the exit."""
        if self.mode != MODE_VICTORY:
            return

        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((15, 23, 42, 180))  # Semi-transparent backdrop
        self.screen.blit(overlay, (0, 0))

        # Victory dialog box
        box_w = 460
        box_h = 240
        box_rect = pygame.Rect((self.width - box_w) // 2, (self.height - box_h) // 2, box_w, box_h)
        pygame.draw.rect(self.screen, (30, 41, 59), box_rect, border_radius=12)
        pygame.draw.rect(self.screen, (74, 222, 128), box_rect, width=3, border_radius=12)

        v_title = self.font_title.render("MAZE ESCAPED! VICTORY!", True, (74, 222, 128))
        self.screen.blit(v_title, v_title.get_rect(center=(box_rect.centerx, box_rect.y + 40)))

        msg1 = self.font_body.render(f"Congratulations! You guided the player to the exit in {self.player_moves} moves.", True, COLOR_TEXT_WHITE)
        self.screen.blit(msg1, msg1.get_rect(center=(box_rect.centerx, box_rect.y + 85)))

        msg2 = self.font_body.render("Compare your path with BFS (shortest) and DFS algorithms!", True, COLOR_TEXT_MUTED)
        self.screen.blit(msg2, msg2.get_rect(center=(box_rect.centerx, box_rect.y + 115)))

        hint1 = self.font_bold.render("Press 'G' for a New Maze  |  Press 'R' to Replay", True, COLOR_TEXT_ACCENT)
        self.screen.blit(hint1, hint1.get_rect(center=(box_rect.centerx, box_rect.y + 160)))

        hint2 = self.font_mini.render("Click anywhere or press any key to dismiss this message.", True, COLOR_TEXT_MUTED)
        self.screen.blit(hint2, hint2.get_rect(center=(box_rect.centerx, box_rect.y + 195)))

    def run(self):
        """Main application game loop."""
        running = True
        while running:
            # Handle Pygame Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Dismiss victory modal on mouse click or key press
                if self.mode == MODE_VICTORY:
                    if event.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN):
                        self.mode = MODE_PLAY
                        continue

                # Button event handling
                if self.btn_play.handle_event(event):
                    self.mode = MODE_PLAY
                    self.status_message = "Play Mode activated. Use WASD or Arrow Keys to move."
                elif self.btn_new_maze.handle_event(event):
                    self.new_maze()
                elif self.btn_dfs.handle_event(event):
                    self.start_dfs_solver()
                elif self.btn_bfs.handle_event(event):
                    self.start_bfs_solver()
                elif self.btn_reset.handle_event(event):
                    self.reset_player()
                elif self.btn_instant.handle_event(event):
                    self.instant_complete_solver()

                # Keyboard controls
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        self.handle_player_move(-1, 0)
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        self.handle_player_move(1, 0)
                    elif event.key in (pygame.K_LEFT, pygame.K_a):
                        self.handle_player_move(0, -1)
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        self.handle_player_move(0, 1)
                    elif event.key == pygame.K_g:
                        self.new_maze()
                    elif event.key in (pygame.K_1,):
                        self.start_dfs_solver()
                    elif event.key in (pygame.K_2,):
                        self.start_bfs_solver()
                    elif event.key == pygame.K_r:
                        self.reset_player()
                    elif event.key == pygame.K_SPACE:
                        self.instant_complete_solver()
                    elif event.key == pygame.K_ESCAPE:
                        running = False

            # Update animation step
            self.update_animation()

            # Render frame
            self.screen.fill(COLOR_BG)
            self.draw_top_bar()
            self.draw_maze()
            self.draw_side_panel()
            self.draw_victory_overlay()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


def main():
    """Application entry point."""
    if "--test" in sys.argv:
        print("Self-test mode: Initializing MazeGameApp...")
        app = MazeGameApp(screen_width=1040, screen_height=700, maze_size=21)
        app.start_dfs_solver()
        app.instant_complete_solver()
        app.start_bfs_solver()
        app.instant_complete_solver()
        assert app.bfs_result.found and app.dfs_result.found
        assert app.bfs_result.path_length <= app.dfs_result.path_length
        print("Self-test passed successfully! All modules operating normally.")
        pygame.quit()
        return

    app = MazeGameApp(screen_width=1040, screen_height=700, maze_size=21)
    app.run()


if __name__ == "__main__":
    main()
