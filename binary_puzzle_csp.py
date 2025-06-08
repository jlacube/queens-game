"""
Binary Puzzle Solver using the CSP framework

This module implements a binary puzzle game with the following rules:
- 6x6 board
- Each cell contains only 1 of 2 items type: O or >
- No more than 2 O or 2 > may be next to each other, either vertically or horizontally
- Each row and each column must contain 3 O and 3 >
- Constraints between cells:
  - x means the symbol is opposite on each side of the x
  - = means it's the same symbol on each side of the =
  - If no constraint between 2 cells, use a dot (.)
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from csp_solver import CSP
import time

class BinaryPuzzleCSP(CSP):
    """
    Binary Puzzle CSP: Fill a 6x6 grid with O and > symbols according to the rules.
    """
    
    def __init__(self, horizontal_constraints=None, vertical_constraints=None, initial_board=None):
        """
        Initialize the Binary Puzzle CSP.
        
        Args:
            horizontal_constraints: 6x5 grid of constraints between horizontal cells ('x', '=', or '.')
            vertical_constraints: 5x6 grid of constraints between vertical cells ('x', '=', or '.')
            initial_board: 6x6 grid with initial values (None for empty cells, 'O' or '>' for filled cells)
        """
        self.size = 6
        
        # Initialize the board with None (empty) or given values
        if initial_board is None:
            self.board = [[None for _ in range(self.size)] for _ in range(self.size)]
        else:
            self.board = initial_board
        
        # Initialize constraints
        if horizontal_constraints is None:
            # Default: no constraints
            self.horizontal_constraints = [['.' for _ in range(self.size-1)] for _ in range(self.size)]
        else:
            self.horizontal_constraints = horizontal_constraints
        
        if vertical_constraints is None:
            # Default: no constraints
            self.vertical_constraints = [['.' for _ in range(self.size)] for _ in range(self.size-1)]
        else:
            self.vertical_constraints = vertical_constraints
        
        # Symbol mapping
        self.symbols = ['O', '>']
        
        # For forward checking
        self.current_domains = {}
        
        super().__init__()
    
    def get_variables(self):
        """Variables are the cells in the grid (row, col)"""
        variables = []
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] is None:  # Only empty cells are variables
                    variables.append((i, j))
        return variables
    
    def get_domains(self):
        """Domain for each cell is the set of possible symbols (O, >)"""
        return {var: self.symbols.copy() for var in self.variables}
    
    def get_constraints(self):
        """Define the constraints for the Binary Puzzle"""
        # For this puzzle, we'll implement the constraints directly in is_consistent
        # This is more efficient than checking all constraints for each assignment
        return []
    
    def select_unassigned_variable(self):
        """
        Select an unassigned variable using a combination of heuristics:
        1. Minimum Remaining Values (MRV): Choose the variable with the fewest legal values
        2. Degree: Break ties by choosing the variable involved in the most constraints
        """
        unassigned = [v for v in self.variables if v not in self.assignment]
        
        # Calculate legal values for each unassigned variable
        legal_values = {}
        for var in unassigned:
            legal_values[var] = sum(1 for value in self.domains[var] if self.is_consistent(var, value))
        
        # Find variables with minimum remaining values
        min_remaining = min(legal_values.values())
        mrv_vars = [var for var, count in legal_values.items() if count == min_remaining]
        
        if len(mrv_vars) == 1:
            return mrv_vars[0]
        
        # Break ties using degree heuristic (most constraints)
        def count_constraints(var):
            row, col = var
            count = 0
            
            # Count horizontal constraints
            if col > 0 and self.horizontal_constraints[row][col-1] != '.':
                count += 1
            if col < self.size - 1 and self.horizontal_constraints[row][col] != '.':
                count += 1
            
            # Count vertical constraints
            if row > 0 and self.vertical_constraints[row-1][col] != '.':
                count += 1
            if row < self.size - 1 and self.vertical_constraints[row][col] != '.':
                count += 1
            
            return count
        
        return max(mrv_vars, key=count_constraints)
    
    def order_domain_values(self, var):
        """
        Order domain values to try the most promising values first.
        Use the least constraining value heuristic: prefer values that rule out the fewest choices for neighboring variables.
        """
        row, col = var
        
        # Create a temporary board with the current assignment
        temp_board = [row[:] for row in self.board]
        for (r, c), v in self.assignment.items():
            temp_board[r][c] = v
        
        # For each value, count how many options it eliminates for neighboring variables
        def count_eliminated_options(value):
            # Assign the value temporarily
            temp_board[row][col] = value
            
            # Count eliminated options for neighbors
            eliminated = 0
            
            # Check neighbors in the same row
            for c in range(self.size):
                if c != col and temp_board[row][c] is None and (row, c) not in self.assignment:
                    for val in self.symbols:
                        temp_board[row][col] = value
                        if not self._is_consistent_for_neighbor((row, c), val, temp_board):
                            eliminated += 1
            
            # Check neighbors in the same column
            for r in range(self.size):
                if r != row and temp_board[r][col] is None and (r, col) not in self.assignment:
                    for val in self.symbols:
                        temp_board[row][col] = value
                        if not self._is_consistent_for_neighbor((r, col), val, temp_board):
                            eliminated += 1
            
            # Reset the temporary assignment
            temp_board[row][col] = None
            
            return eliminated
        
        # Sort values by the number of options they eliminate (ascending)
        return sorted(self.domains[var], key=count_eliminated_options)
    
    def _is_consistent_for_neighbor(self, var, value, temp_board):
        """Helper method to check consistency for a neighbor during domain value ordering"""
        row, col = var
        
        # Make a copy of the board with the value assigned
        board_copy = [r[:] for r in temp_board]
        board_copy[row][col] = value
        
        # Check row sequence
        row_values = [board_copy[row][c] for c in range(self.size) if board_copy[row][c] is not None]
        if not self._check_sequence(row_values):
            return False
        
        # Check column sequence
        col_values = [board_copy[r][col] for r in range(self.size) if board_copy[r][col] is not None]
        if not self._check_sequence(col_values):
            return False
        
        # Check row counts
        row_o_count = sum(1 for c in range(self.size) if board_copy[row][c] == 'O')
        row_gt_count = sum(1 for c in range(self.size) if board_copy[row][c] == '>')
        if row_o_count > 3 or row_gt_count > 3:
            return False
        
        # Check column counts
        col_o_count = sum(1 for r in range(self.size) if board_copy[r][col] == 'O')
        col_gt_count = sum(1 for r in range(self.size) if board_copy[r][col] == '>')
        if col_o_count > 3 or col_gt_count > 3:
            return False
        
        return True
    
    def is_consistent(self, var, value):
        """
        Check if assigning value to var is consistent with current assignment and constraints.
        
        Args:
            var: (row, col) tuple
            value: 'O' or '>'
        """
        row, col = var
        
        # Create a temporary board with the current assignment and the new value
        temp_board = [row[:] for row in self.board]
        for (r, c), v in self.assignment.items():
            temp_board[r][c] = v
        temp_board[row][col] = value
        
        # Check row constraints
        row_values = [temp_board[row][c] for c in range(self.size) if temp_board[row][c] is not None]
        if not self._check_sequence(row_values):
            return False
        
        # Count symbols in the row
        row_o_count = sum(1 for c in range(self.size) if temp_board[row][c] == 'O')
        row_gt_count = sum(1 for c in range(self.size) if temp_board[row][c] == '>')
        
        # Check if we've exceeded the maximum allowed symbols per row
        if row_o_count > 3 or row_gt_count > 3:
            return False
        
        # Check if we've filled the row and have the correct counts
        if row_o_count + row_gt_count == self.size and (row_o_count != 3 or row_gt_count != 3):
            return False
        
        # Check column constraints
        col_values = [temp_board[r][col] for r in range(self.size) if temp_board[r][col] is not None]
        if not self._check_sequence(col_values):
            return False
        
        # Count symbols in the column
        col_o_count = sum(1 for r in range(self.size) if temp_board[r][col] == 'O')
        col_gt_count = sum(1 for r in range(self.size) if temp_board[r][col] == '>')
        
        # Check if we've exceeded the maximum allowed symbols per column
        if col_o_count > 3 or col_gt_count > 3:
            return False
        
        # Check if we've filled the column and have the correct counts
        if col_o_count + col_gt_count == self.size and (col_o_count != 3 or col_gt_count != 3):
            return False
        
        # Check horizontal constraints between cells
        if col > 0:
            left_cell = temp_board[row][col-1]
            constraint = self.horizontal_constraints[row][col-1]
            if left_cell is not None:
                if constraint == 'x' and left_cell == value:
                    return False
                if constraint == '=' and left_cell != value:
                    return False
        
        if col < self.size - 1:
            right_cell = temp_board[row][col+1]
            constraint = self.horizontal_constraints[row][col]
            if right_cell is not None:
                if constraint == 'x' and right_cell == value:
                    return False
                if constraint == '=' and right_cell != value:
                    return False
        
        # Check vertical constraints between cells
        if row > 0:
            above_cell = temp_board[row-1][col]
            constraint = self.vertical_constraints[row-1][col]
            if above_cell is not None:
                if constraint == 'x' and above_cell == value:
                    return False
                if constraint == '=' and above_cell != value:
                    return False
        
        if row < self.size - 1:
            below_cell = temp_board[row+1][col]
            constraint = self.vertical_constraints[row][col]
            if below_cell is not None:
                if constraint == 'x' and below_cell == value:
                    return False
                if constraint == '=' and below_cell != value:
                    return False
        
        return True
    
    def solve(self, timeout=30) -> bool:
        """
        Solve the CSP using backtracking with forward checking and a timeout.
        
        Args:
            timeout: Maximum time in seconds to spend on solving
        """
        # Initialize current domains for forward checking
        self.current_domains = {var: list(self.domains[var]) for var in self.variables}
        
        start_time = time.time()
        result = self._backtrack_with_forward_checking(start_time, timeout)
        end_time = time.time()
        
        if result:
            print(f"Solution found in {end_time - start_time:.4f} seconds")
            return True
        else:
            if end_time - start_time >= timeout:
                print(f"Timeout after {timeout} seconds")
            else:
                print("No solution exists")
            return False
    
    def _backtrack_with_forward_checking(self, start_time, timeout) -> bool:
        """Backtracking algorithm with forward checking to find a solution"""
        # Check timeout
        if time.time() - start_time >= timeout:
            return False
        
        if self.is_complete():
            return True
        
        var = self.select_unassigned_variable()
        
        for value in self.order_domain_values(var):
            if self.is_consistent(var, value):
                # Assign value to var
                self.assignment[var] = value
                
                # Save current domains
                saved_domains = {v: list(self.current_domains[v]) for v in self.variables if v != var}
                
                # Forward checking: Update domains of unassigned variables
                if self._forward_check(var, value):
                    # Recursively try to complete the assignment
                    if self._backtrack_with_forward_checking(start_time, timeout):
                        return True
                
                # If we get here, this assignment didn't work
                del self.assignment[var]
                
                # Restore domains
                for v in saved_domains:
                    self.current_domains[v] = saved_domains[v]
        
        return False
    
    def _forward_check(self, var, value) -> bool:
        """
        Update domains of unassigned variables based on the assignment of value to var.
        Return False if any domain becomes empty.
        """
        row, col = var
        
        # Check rows and columns
        for i in range(self.size):
            # Check row
            if i != col and (row, i) in self.variables and (row, i) not in self.assignment:
                if not self._revise_domain((row, i), var, value):
                    return False
            
            # Check column
            if i != row and (i, col) in self.variables and (i, col) not in self.assignment:
                if not self._revise_domain((i, col), var, value):
                    return False
        
        return True
    
    def _revise_domain(self, var2, var1, value1) -> bool:
        """
        Revise the domain of var2 given that var1 = value1.
        Return False if the domain becomes empty.
        """
        row2, col2 = var2
        row1, col1 = var1
        
        revised = False
        to_remove = []
        
        for value2 in self.current_domains[var2]:
            # Create a temporary assignment
            temp_assignment = self.assignment.copy()
            temp_assignment[var1] = value1
            temp_assignment[var2] = value2
            
            # Check if this assignment violates any constraints
            if not self._is_valid_assignment(temp_assignment, var2, value2):
                to_remove.append(value2)
                revised = True
        
        # Remove values from domain
        for value in to_remove:
            self.current_domains[var2].remove(value)
        
        # Check if domain is empty
        return len(self.current_domains[var2]) > 0
    
    def _is_valid_assignment(self, assignment, var, value) -> bool:
        """Check if assigning value to var is valid given the current assignment"""
        row, col = var
        
        # Create a temporary board with the assignment
        temp_board = [[None for _ in range(self.size)] for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] is not None:
                    temp_board[i][j] = self.board[i][j]
        
        for (r, c), v in assignment.items():
            temp_board[r][c] = v
        
        # Check row constraints
        row_values = [temp_board[row][c] for c in range(self.size) if temp_board[row][c] is not None]
        if not self._check_sequence(row_values):
            return False
        
        # Count symbols in the row
        row_o_count = sum(1 for c in range(self.size) if temp_board[row][c] == 'O')
        row_gt_count = sum(1 for c in range(self.size) if temp_board[row][c] == '>')
        
        # Check if we've exceeded the maximum allowed symbols per row
        if row_o_count > 3 or row_gt_count > 3:
            return False
        
        # Check column constraints
        col_values = [temp_board[r][col] for r in range(self.size) if temp_board[r][col] is not None]
        if not self._check_sequence(col_values):
            return False
        
        # Count symbols in the column
        col_o_count = sum(1 for r in range(self.size) if temp_board[r][col] == 'O')
        col_gt_count = sum(1 for r in range(self.size) if temp_board[r][col] == '>')
        
        # Check if we've exceeded the maximum allowed symbols per column
        if col_o_count > 3 or col_gt_count > 3:
            return False
        
        # Check horizontal constraints
        if col > 0 and temp_board[row][col-1] is not None:
            left_cell = temp_board[row][col-1]
            constraint = self.horizontal_constraints[row][col-1]
            if constraint == 'x' and left_cell == value:
                return False
            if constraint == '=' and left_cell != value:
                return False
        
        if col < self.size - 1 and temp_board[row][col+1] is not None:
            right_cell = temp_board[row][col+1]
            constraint = self.horizontal_constraints[row][col]
            if constraint == 'x' and right_cell == value:
                return False
            if constraint == '=' and right_cell != value:
                return False
        
        # Check vertical constraints
        if row > 0 and temp_board[row-1][col] is not None:
            above_cell = temp_board[row-1][col]
            constraint = self.vertical_constraints[row-1][col]
            if constraint == 'x' and above_cell == value:
                return False
            if constraint == '=' and above_cell != value:
                return False
        
        if row < self.size - 1 and temp_board[row+1][col] is not None:
            below_cell = temp_board[row+1][col]
            constraint = self.vertical_constraints[row][col]
            if constraint == 'x' and below_cell == value:
                return False
            if constraint == '=' and below_cell != value:
                return False
        
        return True
    
    def _check_sequence(self, values):
        """
        Check if a sequence of values has no more than 2 consecutive identical symbols.
        
        Args:
            values: List of values ('O', '>', or None)
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
    
    def visualize(self):
        """Visualize the binary puzzle solution"""
        fig, ax = plt.subplots(figsize=(10, 10))
        
        # Create a grid
        for i in range(self.size + 1):
            ax.axhline(i, color='black', linewidth=2)
            ax.axvline(i, color='black', linewidth=2)
        
        # Fill in the symbols
        for i in range(self.size):
            for j in range(self.size):
                if (i, j) in self.assignment:
                    symbol = self.assignment[(i, j)]
                else:
                    symbol = self.board[i][j] if self.board[i][j] is not None else ''
                
                # Ensure symbol is a string
                symbol_str = str(symbol) if symbol is not None else ''
                
                ax.text(j + 0.5, self.size - i - 0.5, symbol_str,
                        fontsize=24, ha='center', va='center')
        
        # Add horizontal constraints
        for i in range(self.size):
            for j in range(self.size - 1):
                constraint = self.horizontal_constraints[i][j]
                if constraint != '.':
                    ax.text(j + 1, self.size - i - 0.5, constraint, 
                            fontsize=16, ha='center', va='center', color='red')
        
        # Add vertical constraints
        for i in range(self.size - 1):
            for j in range(self.size):
                constraint = self.vertical_constraints[i][j]
                if constraint != '.':
                    ax.text(j + 0.5, self.size - i - 1, constraint, 
                            fontsize=16, ha='center', va='center', color='red')
        
        # Set limits and remove ticks
        ax.set_xlim(0, self.size)
        ax.set_ylim(0, self.size)
        ax.set_xticks([])
        ax.set_yticks([])
        
        plt.title("Binary Puzzle Solution")
        plt.tight_layout()
        plt.savefig("binary_puzzle_solution.png")
        plt.show()
    
    def get_solution_board(self):
        """Convert the assignment to a board representation"""
        solution = [row[:] for row in self.board]
        for (row, col), value in self.assignment.items():
            solution[row][col] = value
        return solution