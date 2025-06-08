"""
Step-by-Step Binary Puzzle Solver that builds the solution incrementally
"""

from binary_puzzle_csp import BinaryPuzzleCSP
import time
import copy
from typing import List, Dict, Tuple, Optional, Any, Union

class StepByStepSolver:
    """
    Step-by-Step Binary Puzzle Solver that builds the solution incrementally
    """
    
    def __init__(self, horizontal_constraints, vertical_constraints, initial_board, guide_solution=None):
        """
        Initialize the solver with constraints, initial board, and optional guide solution
        """
        self.size = 6
        self.horizontal_constraints = horizontal_constraints
        self.vertical_constraints = vertical_constraints
        self.initial_board = initial_board
        self.guide_solution = guide_solution
        self.current_board = copy.deepcopy(initial_board)
        self.debug_level = 2  # 0: no debug, 1: basic, 2: detailed
    
    def solve(self):
        """
        Solve the puzzle step by step
        """
        print("Starting step-by-step solver...")
        
        # Step 1: Fill in the initial board
        print("\nStep 1: Initial board")
        self._print_board(self.current_board)
        
        # Step 2: Apply constraint propagation
        print("\nStep 2: Apply constraint propagation")
        if not self._apply_constraint_propagation():
            print("No solution exists (detected during constraint propagation)")
            return False
        
        # Step 3: Try to solve cell by cell
        print("\nStep 3: Solve cell by cell")
        if not self._solve_cell_by_cell():
            print("No solution exists (detected during cell-by-cell solving)")
            return False
        
        # Step 4: Verify the solution
        print("\nStep 4: Verify the solution")
        if self._verify_solution():
            print("Solution found!")
            return True
        else:
            print("Invalid solution")
            return False
    
    def _apply_constraint_propagation(self):
        """
        Apply constraint propagation to fill in obvious cells
        """
        board: List[List[Optional[str]]] = self.current_board
        
        # Apply constraint propagation until no more changes
        changed = True
        iteration = 0
        while changed:
            iteration += 1
            if self.debug_level >= 1:
                print(f"Constraint propagation iteration {iteration}")
            
            changed = False
            
            # Apply opportunity of elimination
            for i in range(self.size):
                for j in range(self.size):
                    if board[i][j] is None:
                        # Check row for two consecutive identical symbols
                        if j >= 2 and board[i][j-1] == board[i][j-2] and board[i][j-1] is not None:
                            # Must place the opposite symbol
                            opposite = '>' if board[i][j-1] == 'O' else 'O'
                            board[i][j] = opposite
                            changed = True
                            if self.debug_level >= 2:
                                print(f"Found two consecutive {board[i][j-1]} at ({i+1},{j-1}) and ({i+1},{j-2}), placing {opposite} at ({i+1},{j+1})")
                        elif j <= self.size-3 and board[i][j+1] == board[i][j+2] and board[i][j+1] is not None:
                            # Must place the opposite symbol
                            opposite = '>' if board[i][j+1] == 'O' else 'O'
                            board[i][j] = opposite
                            changed = True
                            if self.debug_level >= 2:
                                print(f"Found two consecutive {board[i][j+1]} at ({i+1},{j+2}) and ({i+1},{j+3}), placing {opposite} at ({i+1},{j+1})")
                        
                        # Check column for two consecutive identical symbols
                        if i >= 2 and board[i-1][j] == board[i-2][j] and board[i-1][j] is not None:
                            # Must place the opposite symbol
                            opposite = '>' if board[i-1][j] == 'O' else 'O'
                            board[i][j] = opposite
                            changed = True
                            if self.debug_level >= 2:
                                print(f"Found two consecutive {board[i-1][j]} at ({i},{j+1}) and ({i-1},{j+1}), placing {opposite} at ({i+1},{j+1})")
                        elif i <= self.size-3 and board[i+1][j] == board[i+2][j] and board[i+1][j] is not None:
                            # Must place the opposite symbol
                            opposite = '>' if board[i+1][j] == 'O' else 'O'
                            board[i][j] = opposite
                            changed = True
                            if self.debug_level >= 2:
                                print(f"Found two consecutive {board[i+1][j]} at ({i+2},{j+1}) and ({i+3},{j+1}), placing {opposite} at ({i+1},{j+1})")
            
            # Check for row/column balance (if a row/column has 3 of one symbol, the rest must be the other)
            for i in range(self.size):
                # Check rows
                row_o_count = sum(1 for j in range(self.size) if board[i][j] == 'O')
                row_gt_count = sum(1 for j in range(self.size) if board[i][j] == '>')
                
                if row_o_count == 3:
                    # Fill remaining cells with '>'
                    for j in range(self.size):
                        if board[i][j] is None:
                            board[i][j] = '>'
                            changed = True
                            if self.debug_level >= 2:
                                print(f"Row {i+1} already has 3 O's, placing > at ({i+1},{j+1})")
                
                if row_gt_count == 3:
                    # Fill remaining cells with 'O'
                    for j in range(self.size):
                        if board[i][j] is None:
                            board[i][j] = 'O'
                            changed = True
                            if self.debug_level >= 2:
                                print(f"Row {i+1} already has 3 >'s, placing O at ({i+1},{j+1})")
                
                # Check columns
                col_o_count = sum(1 for i2 in range(self.size) if board[i2][i] == 'O')
                col_gt_count = sum(1 for i2 in range(self.size) if board[i2][i] == '>')
                
                if col_o_count == 3:
                    # Fill remaining cells with '>'
                    for i2 in range(self.size):
                        if board[i2][i] is None:
                            board[i2][i] = '>'
                            changed = True
                            if self.debug_level >= 2:
                                print(f"Column {i+1} already has 3 O's, placing > at ({i2+1},{i+1})")
                
                if col_gt_count == 3:
                    # Fill remaining cells with 'O'
                    for i2 in range(self.size):
                        if board[i2][i] is None:
                            board[i2][i] = 'O'
                            changed = True
                            if self.debug_level >= 2:
                                print(f"Column {i+1} already has 3 >'s, placing O at ({i2+1},{i+1})")
            
            # Check for constraint violations
            if not self._check_board_validity(board):
                if self.debug_level >= 1:
                    print("Board is invalid after constraint propagation")
                return False
            
            if changed and self.debug_level >= 1:
                print("\nBoard after iteration", iteration)
                self._print_board(board)
        
        return True
    
    def _solve_cell_by_cell(self):
        """
        Solve the puzzle cell by cell, using the guide solution if available
        """
        # Find all empty cells
        empty_cells = []
        for i in range(self.size):
            for j in range(self.size):
                if self.current_board[i][j] is None:
                    empty_cells.append((i, j))
        
        if not empty_cells:
            return True  # Board is already filled
        
        print(f"Found {len(empty_cells)} empty cells to fill")
        
        # Try to fill each empty cell
        for idx, (row, col) in enumerate(empty_cells):
            print(f"\nFilling cell {idx+1}/{len(empty_cells)} at ({row+1},{col+1})")
            
            # Get the guide value for this cell
            guide_value = None
            if self.guide_solution is not None:
                guide_value = self.guide_solution[row][col]
                print(f"Guide value: {guide_value}")
            
            # Try each possible value
            values_to_try = ['O', '>']
            if guide_value in values_to_try:
                # Try the guide value first
                values_to_try.remove(guide_value)
                values_to_try.insert(0, guide_value)
            
            success = False
            for value in values_to_try:
                print(f"Trying {value} at ({row+1},{col+1})")
                
                # Create a temporary board with the value assigned
                temp_board = copy.deepcopy(self.current_board)
                temp_board[row][col] = value
                
                # Check if the board is still valid
                if self._check_board_validity(temp_board):
                    print(f"{value} is valid at ({row+1},{col+1})")
                    self.current_board[row][col] = value
                    success = True
                    break
                else:
                    print(f"{value} is NOT valid at ({row+1},{col+1})")
            
            if not success:
                print(f"No valid value found for ({row+1},{col+1})")
                return False
            
            print("Current board:")
            self._print_board(self.current_board)
        
        return True
    
    def _check_board_validity(self, board):
        """
        Check if the board is valid according to all constraints
        """
        # Check for more than 2 consecutive identical symbols
        for i in range(self.size):
            # Check rows
            row_values = [board[i][j] for j in range(self.size) if board[i][j] is not None]
            if not self._check_sequence(row_values):
                if self.debug_level >= 2:
                    print(f"Row {i+1} has more than 2 consecutive identical symbols")
                return False
            
            # Check columns
            col_values = [board[j][i] for j in range(self.size) if board[j][i] is not None]
            if not self._check_sequence(col_values):
                if self.debug_level >= 2:
                    print(f"Column {i+1} has more than 2 consecutive identical symbols")
                return False
        
        # Check row/column balance
        for i in range(self.size):
            # Check rows
            row_o_count = sum(1 for j in range(self.size) if board[i][j] == 'O')
            row_gt_count = sum(1 for j in range(self.size) if board[i][j] == '>')
            
            if row_o_count > 3:
                if self.debug_level >= 2:
                    print(f"Row {i+1} has more than 3 O's ({row_o_count})")
                return False
            
            if row_gt_count > 3:
                if self.debug_level >= 2:
                    print(f"Row {i+1} has more than 3 >'s ({row_gt_count})")
                return False
            
            # Check if we've filled the row and have the correct counts
            row_filled = sum(1 for j in range(self.size) if board[i][j] is not None)
            if row_filled == self.size and (row_o_count != 3 or row_gt_count != 3):
                if self.debug_level >= 2:
                    print(f"Row {i+1} has {row_o_count} O's and {row_gt_count} >'s (should be 3 each)")
                return False
            
            # Check columns
            col_o_count = sum(1 for j in range(self.size) if board[j][i] == 'O')
            col_gt_count = sum(1 for j in range(self.size) if board[j][i] == '>')
            
            if col_o_count > 3:
                if self.debug_level >= 2:
                    print(f"Column {i+1} has more than 3 O's ({col_o_count})")
                return False
            
            if col_gt_count > 3:
                if self.debug_level >= 2:
                    print(f"Column {i+1} has more than 3 >'s ({col_gt_count})")
                return False
            
            # Check if we've filled the column and have the correct counts
            col_filled = sum(1 for j in range(self.size) if board[j][i] is not None)
            if col_filled == self.size and (col_o_count != 3 or col_gt_count != 3):
                if self.debug_level >= 2:
                    print(f"Column {i+1} has {col_o_count} O's and {col_gt_count} >'s (should be 3 each)")
                return False
        
        # Check horizontal constraints
        for i in range(self.size):
            for j in range(self.size-1):
                constraint = self.horizontal_constraints[i][j]
                if constraint != '.' and board[i][j] is not None and board[i][j+1] is not None:
                    if constraint == 'x' and board[i][j] == board[i][j+1]:
                        if self.debug_level >= 2:
                            print(f"Horizontal constraint 'x' violated at ({i+1},{j+1})")
                        return False
                    if constraint == '=' and board[i][j] != board[i][j+1]:
                        if self.debug_level >= 2:
                            print(f"Horizontal constraint '=' violated at ({i+1},{j+1})")
                        return False
        
        # Check vertical constraints
        for i in range(self.size-1):
            for j in range(self.size):
                constraint = self.vertical_constraints[i][j]
                if constraint != '.' and board[i][j] is not None and board[i+1][j] is not None:
                    if constraint == 'x' and board[i][j] == board[i+1][j]:
                        if self.debug_level >= 2:
                            print(f"Vertical constraint 'x' violated at ({i+1},{j+1})")
                        return False
                    if constraint == '=' and board[i][j] != board[i+1][j]:
                        if self.debug_level >= 2:
                            print(f"Vertical constraint '=' violated at ({i+1},{j+1})")
                        return False
        
        return True
    
    def _check_sequence(self, values):
        """
        Check if a sequence of values has no more than 2 consecutive identical symbols
        """
        # Filter out None values
        values = [v for v in values if v is not None]
        
        # Check for more than 2 consecutive identical symbols
        count = 1
        for i in range(1, len(values)):
            if values[i] == values[i-1]:
                count += 1
                if count > 2:
                    return False
            else:
                count = 1
        
        return True
    
    def _verify_solution(self):
        """
        Verify that the solution is valid
        """
        # Check if the board is completely filled
        for i in range(self.size):
            for j in range(self.size):
                if self.current_board[i][j] is None:
                    print(f"Board is not completely filled (empty cell at ({i+1},{j+1}))")
                    return False
        
        # Check if the board is valid
        if not self._check_board_validity(self.current_board):
            print("Board is not valid")
            return False
        
        # Compare with guide solution if available
        if self.guide_solution is not None:
            matches_guide = True
            for i in range(self.size):
                for j in range(self.size):
                    if self.current_board[i][j] != self.guide_solution[i][j]:
                        matches_guide = False
                        print(f"Solution differs from guide at ({i+1},{j+1}): {self.current_board[i][j]} vs {self.guide_solution[i][j]}")
            
            if matches_guide:
                print("Solution matches the guide solution")
            else:
                print("Solution differs from the guide solution, but may still be valid")
        
        return True
    
    def _print_board(self, board):
        """Print the current state of the board"""
        for i in range(self.size):
            row_str = ""
            for j in range(self.size):
                cell = board[i][j]
                if cell is None:
                    row_str += ". "
                else:
                    row_str += cell + " "
            print(row_str)

def main():
    print("Step-by-Step Binary Puzzle Solver")
    print("================================\n")
    
    # Get the constraints from binary_puzzle_example.py
    horizontal_constraints = [
        ['.', 'x', '.', '=', '.'],
        ['.', '.', '.', '.', '.'],
        ['.', 'x', '.', 'x', '.'],
        ['.', '=', '.', '=', '.'],
        ['.', '.', '.', '.', '.'],
        ['.', 'x', '.', 'x', '.']
    ]
    
    vertical_constraints = [
        ['.', '.', '.', '.', '.', '.'],
        ['.', '=', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.'],
        ['.', '=', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.']
    ]
    
    # Initial board from binary_puzzle_example.py
    initial_board = [
        ['O', None, None, None, None, 'O'],
        [None, None, None, None, None, None],
        [None, None, None, None, None, None],
        [None, None, None, None, None, None],
        [None, None, None, None, None, None],
        ['O', None, None, None, None, '>']
    ]
    
    # User's solution from verify_user_solution.py
    user_solution = [
        ['O', '>', 'O', '>', '>', 'O'],
        ['>', 'O', 'O', '>', 'O', '>'],
        ['>', 'O', '>', 'O', '>', 'O'],
        ['O', '>', '>', 'O', 'O', '>'],
        ['>', '>', 'O', '>', 'O', 'O'],
        ['O', 'O', '>', 'O', '>', '>']
    ]
    
    print("Initial board:")
    for row in initial_board:
        print(' '.join(cell if cell is not None else '.' for cell in row))
    
    print("\nUser's solution:")
    for row in user_solution:
        print(' '.join(cell for cell in row))
    
    print("\nSolving step by step...")
    solver = StepByStepSolver(horizontal_constraints, vertical_constraints, initial_board, user_solution)
    if solver.solve():
        print("\nFinal solution:")
        solver._print_board(solver.current_board)
    else:
        print("\nNo solution found")

if __name__ == "__main__":
    main()