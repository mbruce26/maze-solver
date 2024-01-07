import random
import time
from cell import Cell

class Maze:
    def __init__(
            self,
            x1,
            y1,
            num_rows,
            num_cols,
            cell_size_x,
            cell_size_y,
            delay = 0.05,
            win = None,
            seed = None,
        ) -> None:
        self._cells = []
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._delay = delay
        self._win = win
        if seed is not None:
            random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()
    
    def _create_cells(self):
        for _ in range(self._num_cols):
            cell_col = []
            for _ in range(self._num_rows):
                cell_col.append(Cell(self._win))
            self._cells.append(cell_col)
        
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

        self._break_entrance_and_exit()

    def _draw_cell(self, i, j):
        if self._win is None:
            return
        self._cells[i][j].draw(
            self._x1 + self._cell_size_x * i, 
            self._y1 + self._cell_size_y * j, 
            self._x1 + self._cell_size_x * (i + 1),
            self._y1 + self._cell_size_y * (j + 1),
            )
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(self._delay)
    
    def _break_entrance_and_exit(self):
        entrance = self._cells[0][0]
        exit = self._cells[self._num_cols - 1][self._num_rows - 1]
        entrance.has_top_wall = False
        self._draw_cell(0, 0)
        exit.has_bottom_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)
    
        
    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            to_visit = []
            # left
            if i > 0 and not self._cells[i - 1][j].visited:
                to_visit.append((i - 1, j))
            # right
            if i < self._num_cols - 1 and not self._cells[i + 1][j].visited:
                to_visit.append((i + 1, j))
            # up
            if j > 0 and not self._cells[i][j - 1].visited:
                to_visit.append((i, j - 1))
            # down
            if j < self._num_rows - 1 and not self._cells[i][j + 1].visited:
                to_visit.append((i, j + 1))
            
            # nowhere to go
            if len(to_visit) == 0:
                self._draw_cell(i, j)
                return

            dir = random.randint(0, len(to_visit) - 1)
            next = to_visit[dir]

            # left
            if next[0] == i - 1:
                self._cells[i][j].has_left_wall = False
                self._cells[i-1][j].has_right_wall = False
            # right
            elif next[0] == i + 1:
                self._cells[i][j].has_right_wall = False
                self._cells[i + 1][j].has_left_wall = False
            # up
            elif next[1] == j - 1:
                self._cells[i][j].has_top_wall = False
                self._cells[i][j - 1].has_bottom_wall = False
            # down
            else:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j + 1].has_top_wall = False
            
            # recursively move
            self._break_walls_r(next[0], next[1])
    
    def _reset_cells_visited(self):
        for i in range(self._num_cols):
            for cell in self._cells[i]:
                cell.visited = False
    
    def solve(self):
        return self._solve_r(i=0, j=0)

    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True
        if (i, j) == (self._num_cols - 1, self._num_rows - 1):
            return True
        # check left exists, has no wall, and not visited
        if i > 0 and not self._cells[i][j].has_left_wall and not self._cells[i - 1][j].visited:
            self._cells[i][j].draw_move(self._cells[i - 1][j])
            if self._solve_r(i - 1, j):
                return True
            # undo if can't go left
            self._cells[i][j].draw_move(self._cells[i - 1][j], undo=True)
        # check right
        if i < self._num_cols - 1 and not self._cells[i][j].has_right_wall and not self._cells[i + 1][j].visited:
            self._cells[i][j].draw_move(self._cells[i + 1][j])
            if self._solve_r(i + 1, j):
                return True
            self._cells[i][j].draw_move(self._cells[i + 1][j], undo=True)
        # check up
        if j > 0 and not self._cells[i][j].has_top_wall and not self._cells[i][j - 1].visited:
            self._cells[i][j].draw_move(self._cells[i][j - 1])
            if self._solve_r(i, j - 1):
                return True
            self._cells[i][j].draw_move(self._cells[i][j - 1], undo=True)
        # check down
        if j < self._num_rows - 1 and not self._cells[i][j].has_bottom_wall and not self._cells[i][j + 1].visited:
            self._cells[i][j].draw_move(self._cells[i][j + 1])
            if self._solve_r(i, j + 1):
                return True
            self._cells[i][j].draw_move(self._cells[i][j + 1], undo=True)
        # no direction to go
        return False

