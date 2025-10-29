import tkinter as tk
import random

# Fibonacci cache for a 4x4 board
FIB_LIST = [1, 1]
for i in range(2, 16):  # 4x4 = 16 tiles
    FIB_LIST.append(FIB_LIST[i - 1] + FIB_LIST[i - 2])
FIB_SET = set(FIB_LIST)
FIB_INDEX = {FIB_LIST[i]: i for i in range(len(FIB_LIST))}

#colors and fonts for design
GRID_COLOR = "#a39489"
EMPTY_CELL_COLOR = "#c2b3a9"
GAME_OVER_FONT_COLOR = "#ffffff"
WINNER_BG = "#ffcc00"
LOSER_BG = "#a39489"

CELL_COLORS = {
    1: "#fcefe6",
    2: "#f2e8cb",
    3: "#f5b682",
    5: "#f29446",
    8: "#ff775c",
    13: "#e64c2e",
    21: "#ede291",
    34: "#fce130",
    55: "#ffdb4a",
    89: "#f0b922",
    144: "#fad74d",
    233: "#f9a602",   
    377: "#ff8c00",   
    610: "#ff4500",   
    987: "#cc0000",   
}

CELL_NUMBER_COLORS = {
    1: "#695c57",
    2: "#695c57",
    3: "#ffffff",
    5: "#ffffff",
    8: "#ffffff",
    13: "#ffffff",
    21: "#ffffff",
    34: "#ffffff",
    55: "#ffffff",
    89: "#ffffff",
    144: "#ffffff",
    233: "#ffffff",   
    377: "#ffffff",  
    610: "#ffffff",  
    987: "#ffffff",
}

class Game(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.master.title("Fibonacci Frenzy - Click to Merge!")
        
        # ===== SCALE FACTOR - CHANGE THIS TO RESIZE EVERYTHING =====
        self.SCALE = 0.7  # Change this value (0.5 = 50%, 1.0 = 100%, 1.5 = 150%)
        # ===========================================================
        
        # Calculate all scaled dimensions
        self.cell_size = 140  # Fixed at 140x140 as requested
        self.cell_padding = int(5 * self.SCALE)
        self.grid_border = int(3 * self.SCALE)
        self.selection_border = int(5 * self.SCALE)
        
        # Calculate grid size
        grid_size = (self.cell_size * 4) + (self.cell_padding * 8) + (self.grid_border * 2)
        window_width = grid_size + int(40 * self.SCALE)
        window_height = grid_size + int(250 * self.SCALE)
        
        self.master.geometry(f"{window_width}x{window_height}")
        
        # Calculate scaled font sizes
        self.fib_title_font = ("Arial", int(16 * self.SCALE), "bold")
        self.fib_seq_font = ("Arial", int(15 * self.SCALE), "bold")
        self.score_label_font = ("Arial", int(14 * self.SCALE), "bold")
        self.score_value_font = ("Arial", int(20 * self.SCALE), "bold")
        self.mode_font = ("Arial", int(14 * self.SCALE), "bold")
        self.diff_button_font = ("Arial", int(10 * self.SCALE), "bold")
        self.restart_font = ("Arial", int(14 * self.SCALE), "bold")
        self.game_over_font = ("Helvetica", int(48 * self.SCALE), "bold")
        
        # Cell number fonts (scaled)
        self.cell_fonts = {
            1: ("Helvetica", int(55 * self.SCALE), "bold"),
            2: ("Helvetica", int(55 * self.SCALE), "bold"),
            3: ("Helvetica", int(55 * self.SCALE), "bold"),
            5: ("Helvetica", int(55 * self.SCALE), "bold"),
            8: ("Helvetica", int(55 * self.SCALE), "bold"),
            13: ("Helvetica", int(50 * self.SCALE), "bold"),
            21: ("Helvetica", int(50 * self.SCALE), "bold"),
            34: ("Helvetica", int(50 * self.SCALE), "bold"),
            55: ("Helvetica", int(50 * self.SCALE), "bold"),
            89: ("Helvetica", int(50 * self.SCALE), "bold"),
            144: ("Helvetica", int(45 * self.SCALE), "bold"),
            233: ("Helvetica", int(45 * self.SCALE), "bold"),
            377: ("Helvetica", int(45 * self.SCALE), "bold"),
            610: ("Helvetica", int(40 * self.SCALE), "bold"),
            987: ("Helvetica", int(40 * self.SCALE), "bold")
        }
        
        self.main_grid = tk.Frame(
            self, bg=GRID_COLOR, bd=self.grid_border, 
            width=grid_size, height=grid_size
        )
        self.main_grid.grid(pady=(int(200 * self.SCALE), 0), padx=(int(20 * self.SCALE), 0))
        
        # Initialize selection state and difficulty first
        self.selected_tiles = []
        self.selection_count = 0
        self.difficulty = "medium"
        self.target_fib = self.get_target_fib()
        
        self.make_GUI()
        self.start_game()

        self.mainloop()

    def make_GUI(self):
        #make grid
        self.cells = []
        for i in range(4):
            row = []
            for j in range(4):
                cell_frame = tk.Frame(
                    self.main_grid,
                    bg=EMPTY_CELL_COLOR,
                    width=self.cell_size,
                    height=self.cell_size
                )
                cell_frame.grid(row=i, column=j, padx=self.cell_padding, pady=self.cell_padding)
                cell_number = tk.Label(self.main_grid, bg=EMPTY_CELL_COLOR)
                cell_number.grid(row=i, column=j)
                
                # Bind click events to both frame and number label
                cell_frame.bind("<Button-1>", lambda e, r=i, c=j: self.on_cell_click(r, c))
                cell_number.bind("<Button-1>", lambda e, r=i, c=j: self.on_cell_click(r, c))
                
                cell_data = {"frame": cell_frame, "number": cell_number}
                row.append(cell_data)
            self.cells.append(row)
        
        #make fibonacci sequence display at top
        fib_frame = tk.Frame(self)
        fib_frame.place(relx=0.5, y=int(50 * self.SCALE), anchor="center")
        tk.Label(
            fib_frame,
            text="Fibonacci Sequence:",
            font=self.fib_title_font,
            fg=CELL_NUMBER_COLORS[1]
        ).pack()
        tk.Label(
            fib_frame,
            text="1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987",
            font=self.fib_seq_font,
            fg=CELL_NUMBER_COLORS[1]
        ).pack()
        
        #make score and difficulty buttons on the same line
        control_frame = tk.Frame(self)
        control_frame.place(relx=0.5, y=int(130 * self.SCALE), anchor="center")
        
        # Score on the left
        score_frame = tk.Frame(control_frame)
        score_frame.pack(side="left", padx=int(20 * self.SCALE))
        tk.Label(
            score_frame,
            text="Score",
            font=self.score_label_font,
            fg=CELL_NUMBER_COLORS[1]
        ).pack()
        self.score_label = tk.Label(score_frame, text="0", font=self.score_value_font, fg=CELL_NUMBER_COLORS[1])
        self.score_label.pack()
        
        # Difficulty buttons in the center
        diff_frame = tk.Frame(control_frame)
        diff_frame.pack(side="left", padx=int(20 * self.SCALE))
        
        tk.Label(
            diff_frame,
            text="Mode:",
            font=self.mode_font,
            fg=CELL_NUMBER_COLORS[1]
        ).pack()
        
        # Create difficulty buttons in a row
        difficulties = [("easy", 34), ("medium", 89), ("hard", 233), ("super_hard", 987)]
        self.diff_buttons = {}
        
        button_frame = tk.Frame(diff_frame)
        button_frame.pack(pady=int(5 * self.SCALE))
        
        for diff, target in difficulties:
            btn = tk.Button(
                button_frame,
                text=f"{diff.replace('_', ' ').title()}\n{target}",
                command=lambda d=diff: self.change_difficulty(d),
                font=self.diff_button_font,
                bg=CELL_COLORS[1] if diff == self.difficulty else EMPTY_CELL_COLOR,
                fg=CELL_NUMBER_COLORS[1],
                width=int(8 * self.SCALE),
                height=2,
                relief="raised",
                bd=int(2 * self.SCALE)
            )
            btn.pack(side="left", padx=int(3 * self.SCALE))
            self.diff_buttons[diff] = btn
        
        # Restart button on the right
        restart_frame = tk.Frame(control_frame)
        restart_frame.pack(side="left", padx=int(20 * self.SCALE))
        
        restart_btn = tk.Button(
            restart_frame,
            text="Restart",
            command=self.restart_game,
            font=self.restart_font,
            bg=CELL_COLORS[2],
            fg=CELL_NUMBER_COLORS[2],
            relief="raised",
            bd=int(3 * self.SCALE),
            width=int(8 * self.SCALE),
            height=2
        )
        restart_btn.pack()

    def start_game(self):
        # Initialize matrix with zeros
        self.matrix = [[0]*4 for _ in range(4)]
        
        # Fill grid with 15 starting tiles (leaving 1 empty)
        starting_tiles = [1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 5, 5, 8, 8, 13]
        
        # Get all positions and shuffle
        positions = [(i, j) for i in range(4) for j in range(4)]
        random.shuffle(positions)
        
        # Place the starting tiles
        for idx, value in enumerate(starting_tiles):
            row, col = positions[idx]
            self.matrix[row][col] = value
            self.cells[row][col]["frame"].configure(bg=CELL_COLORS[value])
            self.cells[row][col]["number"].configure(
                bg=CELL_COLORS[value],
                fg=CELL_NUMBER_COLORS[value],
                font=self.cell_fonts[value],
                text=str(value)
            )

        self.score = 0
        self.selection_count = 0
        self.selected_tiles = []
        self.target_fib = self.get_target_fib()
        self.update_GUI()

    def update_GUI(self):
        for i in range(4):
            for j in range(4):
                cell_value = self.matrix[i][j]
                if cell_value == 0:
                    self.cells[i][j]["frame"].configure(bg=EMPTY_CELL_COLOR)
                    self.cells[i][j]["number"].configure(bg=EMPTY_CELL_COLOR, text="")
                else:
                    self.cells[i][j]["frame"].configure(bg=CELL_COLORS[cell_value])
                    self.cells[i][j]["number"].configure(
                        bg=CELL_COLORS[cell_value],
                        fg=CELL_NUMBER_COLORS[cell_value],
                        font=self.cell_fonts[cell_value],
                        text=str(cell_value)
                    )
        self.score_label.configure(text=self.score)
        self.update_idletasks()

    def on_cell_click(self, row, col):
        """Handle cell click for tile selection and merging"""
        if self.matrix[row][col] == 0:
            return
            
        if (row, col) in self.selected_tiles:
            self.deselect_tile(row, col)
            return
            
        if self.selection_count >= 2:
            self.clear_selection()
            
        self.select_tile(row, col)
        
        if self.selection_count == 2:
            self.attempt_merge()
    
    def select_tile(self, row, col):
        """Select a tile and add visual highlighting"""
        self.selected_tiles.append((row, col))
        self.selection_count += 1
        self.cells[row][col]["frame"].configure(relief="raised", bd=self.selection_border)
        
    def deselect_tile(self, row, col):
        """Deselect a tile and remove highlighting"""
        if (row, col) in self.selected_tiles:
            self.selected_tiles.remove((row, col))
            self.selection_count -= 1
            self.cells[row][col]["frame"].configure(relief="flat", bd=0)
            
    def clear_selection(self):
        """Clear all tile selections"""
        for row, col in self.selected_tiles:
            self.cells[row][col]["frame"].configure(relief="flat", bd=0)
        self.selected_tiles = []
        self.selection_count = 0
        
    def attempt_merge(self):
        """Try to merge the two selected tiles"""
        if len(self.selected_tiles) != 2:
            return
            
        (r1, c1), (r2, c2) = self.selected_tiles
        val1, val2 = self.matrix[r1][c1], self.matrix[r2][c2]
        
        if self.can_merge(val1, val2):
            merged_value = val1 + val2
            self.matrix[r2][c2] = merged_value
            self.matrix[r1][c1] = 0
            self.score += merged_value
            self.clear_selection()
            self.update_GUI()
            self.game_over()
        else:
            self.clear_selection()
            
    def can_merge(self, val1, val2):
        """Check if two values can be merged (consecutive Fibonacci numbers)"""
        if val1 not in FIB_INDEX or val2 not in FIB_INDEX:
            return False
        if val1 == 1 and val2 == 1:
            return True
        return abs(FIB_INDEX[val1] - FIB_INDEX[val2]) == 1
    
    def get_target_fib(self):
        """Get target Fibonacci number based on difficulty"""
        targets = {
            "easy": 34,
            "medium": 89,
            "hard": 233,
            "super_hard": 987
        }
        return targets.get(self.difficulty, 89)
    
    def change_difficulty(self, difficulty):
        """Change difficulty and update target"""
        self.difficulty = difficulty
        self.target_fib = self.get_target_fib()
        
        for diff, btn in self.diff_buttons.items():
            if diff == difficulty:
                btn.configure(bg=CELL_COLORS[1])
            else:
                btn.configure(bg=EMPTY_CELL_COLOR)
    
    def restart_game(self):
        """Restart the game"""
        for widget in self.main_grid.winfo_children():
            if isinstance(widget, tk.Frame) and len(widget.winfo_children()) == 1:
                label = widget.winfo_children()[0]
                if isinstance(label, tk.Label) and label.cget("text") in ("You Win!", "Game Over!"):
                    widget.destroy()
        self.start_game()
        self.clear_selection()

    def any_move_exists(self):
        """Check if any two tiles can be merged anywhere on the board"""
        tiles = []
        for i in range(4):
            for j in range(4):
                if self.matrix[i][j] != 0:
                    tiles.append(self.matrix[i][j])
        
        if len(tiles) < 2:
            return False
        
        for i in range(len(tiles)):
            for j in range(i + 1, len(tiles)):
                if self.can_merge(tiles[i], tiles[j]):
                    return True
        return False

    def game_over(self):
        """Check if game is over and if win/lose"""
        if any(self.target_fib in row for row in self.matrix):
            game_over_frame = tk.Frame(self.main_grid, borderwidth=int(2 * self.SCALE))
            game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
            tk.Label(
                game_over_frame,
                text="You Win!",
                bg=WINNER_BG,
                fg=GAME_OVER_FONT_COLOR,
                font=self.game_over_font
            ).pack()
        elif not self.any_move_exists():
            game_over_frame = tk.Frame(self.main_grid, borderwidth=int(2 * self.SCALE))
            game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
            tk.Label(
                game_over_frame,
                text="Game Over!",
                bg=LOSER_BG,
                fg=GAME_OVER_FONT_COLOR,
                font=self.game_over_font
            ).pack()

def main():
    Game()

if __name__ == "__main__":
    main()