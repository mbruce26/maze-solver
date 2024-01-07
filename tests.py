import unittest

from maze import Maze


class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells), 
            num_cols
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows
        )
    def test_maze_create_cells_large(self):
        num_cols = 16
        num_rows = 12
        m2 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m2._cells), 
            num_cols
        )
        self.assertEqual(
            len(m2._cells[0]),
            num_rows
        )
    def test_maze_break_walls_r(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        m1._break_walls_r(0, 0)
        for i in range(num_cols):
            for j in range(num_rows):
                self.assertEqual(
                    m1._cells[i][j].visited,
                    True
                )
    def test_maze_reset_cells_visited(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        m1._break_walls_r(0, 0)
        m1._reset_cells_visited()
        for i in range(num_cols):
            for j in range(num_rows):
                self.assertEqual(
                    m1._cells[i][j].visited,
                    False
                )

if __name__ == "__main__":
    unittest.main()