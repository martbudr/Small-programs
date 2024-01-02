import tkinter as tk
import colors as c
import random

BOARD_SIZE = 4

class Game(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.master.title("2048")
        self.configure(bg=c.BG_COLOR)
        self.score = 0
        
        self.main_grid = tk.Frame(
            self,
            bg=c.BG_COLOR
        )
        self.main_grid.grid(pady=(100, 0))
        
        self.master.bind("<Left>", self.left_pressed)
        self.master.bind("<Right>", self.right_pressed)
        self.master.bind("<Up>", self.up_pressed)
        self.master.bind("<Down>", self.down_pressed)
        
        self._create_menu()
        self.make_gui()
        self.start_game()
    
    def _create_menu(self):
        menu_bar = tk.Menu(self)
        self.master.config(menu=menu_bar)
        file_menu = tk.Menu(menu_bar)
        file_menu.add_command(
            label="Restart game",
            command=self.reset_board
        )
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=quit)
        menu_bar.add_cascade(label="File", menu=file_menu)
    
    def reset_board(self):
        self.score_text.config(
            text="Score: ",
            fg=c.SCORE_COLOR
        )
        self.score = 0
        self.score_lbl.configure(text=self.score)
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                self.matrix[i][j] = 0
                self.cells[i][j]["frame"].configure(
                    bg=c.EMPTY_CELL_COLOR
                )
                self.cells[i][j]["number"].configure(
                    text="",
                    bg=c.EMPTY_CELL_COLOR
                )
        self.update_idletasks()
                
        self.start_game()
    
    def make_gui(self):
        score_frm = tk.Frame(
            self,
            bg=c.BG_COLOR
        )
        score_frm.place(relx=0.5, y=45, anchor="center")
        self.score_text = tk.Label(
            score_frm,
            text="Score: ",
            font=c.SCORE_FONT,
            fg=c.SCORE_COLOR,
            bg=c.BG_COLOR
        )
        self.score_text.grid(row=0, column=0)
        self.score_lbl = tk.Label(
            score_frm,
            text=self.score,
            font=c.SCORE_FONT,
            bg=c.BG_COLOR,
            fg=c.SCORE_COLOR
        )
        self.score_lbl.grid(row=0, column=1)
        
        main_frm = tk.Frame(
            self.main_grid,
            bg=c.BG_COLOR
        )
        main_frm.grid(pady=10)
        
        # 2d table containing all grids' info
        self.cells = []
        for i in range(BOARD_SIZE):
            row = []
            for j in range(BOARD_SIZE):
                cell_frm = tk.Frame(
                    main_frm,
                    bg=c.EMPTY_CELL_COLOR,
                    width=100,
                    height=100
                )
                cell_frm.grid(row=i, column=j, padx=5, pady=5)
                cell_num = tk.Label(
                    main_frm,
                    bg=c.EMPTY_CELL_COLOR,
                    text="",
                    font=c.CELL_FONT
                )
                cell_num.grid(row=i, column=j)
                cell_data = {"frame": cell_frm, "number": cell_num}
                row.append(cell_data)
            self.cells.append(row)

    def start_game(self):
        self.matrix = [[0] * BOARD_SIZE for _ in range (BOARD_SIZE)]
        
        for i in range(2):
            self._draw_cell()
        
    def _draw_cell(self):
        row = random.randint(0, BOARD_SIZE-1)
        col = random.randint(0, BOARD_SIZE-1)
        
        while self.matrix[row][col] != 0:
            row = random.randint(0, BOARD_SIZE-1)
            col = random.randint(0, BOARD_SIZE-1)
            
        rand = random.choices([2, 4], [0.95, 0.05])[0]
        self.matrix[row][col] = rand
        self.cells[row][col]["frame"].configure(bg=c.CELL_COLORS[rand].color)
        self.cells[row][col]["number"].configure(
            text=rand,
            fg=c.CELL_COLORS[rand].font,
            bg=c.CELL_COLORS[rand].color,
        )
                
    # board manipulation functions
    # a function moving all the numbers to the left
    def move_left(self):
        new_matrix = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        for i in range(BOARD_SIZE):
            fill_position = 0
            for j in range(BOARD_SIZE):
                if self.matrix[i][j] != 0:
                    new_matrix[i][fill_position] = self.matrix[i][j]
                    fill_position += 1
                    
        self.matrix = new_matrix
                    
    # a function merging numbers
    def merge(self):
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE-1):
                if self.matrix[i][j] != 0 and self.matrix[i][j] == self.matrix[i][j+1]:
                    self.score += self.matrix[i][j]
                    self.matrix[i][j] *= 2
                    self.matrix[i][j+1] = 0

    # a function reversing each row
    def reverse(self):
        new_matrix = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                new_matrix[i][j] = self.matrix[i][BOARD_SIZE-1-j]
                
        self.matrix = new_matrix
        
    # a function transposing the board
    def transpose(self):
        new_matrix = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                new_matrix[i][j] = self.matrix[j][i]
        
        self.matrix = new_matrix
    
    def update_GUI(self):
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                cell_val = self.matrix[i][j]
                if cell_val == 0:
                    self.cells[i][j]["frame"].configure(bg=c.EMPTY_CELL_COLOR)
                    self.cells[i][j]["number"].configure(
                        text="",
                        bg=c.EMPTY_CELL_COLOR
                    )
                else:
                    self.cells[i][j]["frame"].configure(bg=c.CELL_COLORS[cell_val].color)
                    self.cells[i][j]["number"].configure(
                        text=cell_val,
                        fg=c.CELL_COLORS[cell_val].font,
                        bg=c.CELL_COLORS[cell_val].color
                    )       
        self.score_lbl.configure(text=self.score)
        self.update_idletasks()
    
    # handling the user input
    def _move(self):
        self.move_left()
        self.merge()
        self.move_left()
        
    def _update(self):
        if any(0 in row for row in self.matrix):
            self._draw_cell()        
        self.update_GUI()
        self.game_over()
    
    def left_pressed(self, event):
        self._move()      
        self._update()
    def right_pressed(self, event):
        self.reverse()
        self._move()
        self.reverse()
        self._update()
    def up_pressed(self, event):
        self.transpose()
        self._move()
        self.transpose()
        self._update()
    def down_pressed(self, event):
        self.transpose()
        self.reverse()
        self._move()
        self.reverse()
        self.transpose()
        self._update()
        
    # check if there is any move that can be made
    def _can_move(self):
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE-1):
                if self.matrix[i][j] == self.matrix[i][j+1]:
                    return True
                
        for i in range(BOARD_SIZE-1):
            for j in range(BOARD_SIZE):
                if self.matrix[i][j] == self.matrix[i+1][j]:
                    return True
        
        return False
    
    def game_over(self):
        # if 2048 appeared on the board:
        if any(2048 in row for row in self.matrix):
            self.score_text.configure(
                text=f"You won! Score: "
            )
        
        # if can make a move:
        if any(0 in row for row in self.matrix) or self._can_move():
            return
        
        # no moves left:
        if any(2048 in row for row in self.matrix):
            self.score_text.configure(
                text="You won! Your final score: ",
                fg=c.WON_FONT_COLOR
            )
        else:
            self.score_text.configure(
                text="You lost! Your final score: ",
                fg=c.LOST_FONT_COLOR
            )
    

def main():
    window = tk.Tk
    game_frm = Game()
    window.mainloop(game_frm)
    
if __name__ == "__main__":
    main()