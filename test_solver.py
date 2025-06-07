"""
Tests for the Queens Game Solver
"""

import unittest
import numpy as np
from queens_solver import QueensGameSolver

class TestQueensSolver(unittest.TestCase):
    def test_valid_position(self):
        """Test the is_valid_position method"""
        # Create a 4x4 board with simple color regions (each row is a color)
        color_regions = np.array([
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [2, 2, 2, 2],
            [3, 3, 3, 3]
        ])
        solver = QueensGameSolver(4, color_regions)
        
        # Place a queen at (0, 0)
        solver.board[0, 0] = 1
        solver.queens_in_color[0] += 1
        
        # Test positions that should be invalid
        # Same row
        self.assertFalse(solver.is_valid_position(0, 2))
        # Same column
        self.assertFalse(solver.is_valid_position(2, 0))
        # Same color
        self.assertFalse(solver.is_valid_position(0, 3))
        # Touching diagonally
        self.assertFalse(solver.is_valid_position(1, 1))
        # Touching horizontally
        self.assertFalse(solver.is_valid_position(0, 1))
        # Touching vertically
        self.assertFalse(solver.is_valid_position(1, 0))
        
        # Test a valid position
        self.assertTrue(solver.is_valid_position(2, 2))
    
    def test_solve_small_board(self):
        """Test solving a small board with a known solution"""
        # 4x4 board with columns as color regions
        color_regions = np.array([
            [0, 1, 2, 3],
            [0, 1, 2, 3],
            [0, 1, 2, 3],
            [0, 1, 2, 3]
        ])
        solver = QueensGameSolver(4, color_regions)
        
        # This board should have a solution
        self.assertTrue(solver.solve())
        
        # Verify constraints
        self._verify_solution(solver)
    
    def test_solve_medium_board(self):
        """Test solving a medium-sized board"""
        # 5x5 board with columns as color regions
        color_regions = np.array([
            [0, 1, 2, 3, 4],
            [0, 1, 2, 3, 4],
            [0, 1, 2, 3, 4],
            [0, 1, 2, 3, 4],
            [0, 1, 2, 3, 4]
        ])
        solver = QueensGameSolver(5, color_regions)
        
        # This board should have a solution
        self.assertTrue(solver.solve())
        
        # Verify constraints
        self._verify_solution(solver)
    
    def _verify_solution(self, solver):
        """Verify that a solution meets all constraints"""
        n = solver.n
        board = solver.board
        color_regions = solver.color_regions
        
        # Check one queen per row
        for row in range(n):
            self.assertEqual(sum(board[row]), 1)
        
        # Check one queen per column
        for col in range(n):
            self.assertEqual(sum(board[:, col]), 1)
        
        # Check one queen per color
        queens_in_color = [0] * n
        for row in range(n):
            for col in range(n):
                if board[row, col] == 1:
                    color = color_regions[row, col]
                    queens_in_color[color] += 1
        
        for color in range(n):
            self.assertEqual(queens_in_color[color], 1)
        
        # Check queens don't touch
        for row1 in range(n):
            for col1 in range(n):
                if board[row1, col1] == 1:
                    for row2 in range(n):
                        for col2 in range(n):
                            if board[row2, col2] == 1 and (row1 != row2 or col1 != col2):
                                # Check distance between queens
                                distance = max(abs(row1 - row2), abs(col1 - col2))
                                self.assertGreater(distance, 1)

if __name__ == "__main__":
    unittest.main()