"""
Debug version of the Enhanced Binary Puzzle Solver with detailed console output
"""

from binary_puzzle_csp import BinaryPuzzleCSP
import time
import copy
from typing import List, Dict, Tuple, Optional, Any, Union

class DebugEnhancedBinaryPuzzleCSP(BinaryPuzzleCSP):
    """
    Debug version of the Enhanced Binary Puzzle CSP with detailed console output
    """
    
    def __init__(self, horizontal_constraints=None, vertical_constraints=None, initial_board=None):
        """Initialize with debug level"""
        super().__init__(horizontal_constraints, vertical_constraints, initial_board)
        self.debug_depth: int = 0  # For indentation in debug output
        self.nodes_explored: int = 0  # Count nodes explored
        # Explicitly define board type to allow string assignments
        self.board: List[List[Optional[str]]] = self.board
    
    def solve(self, timeout=30) -> bool:
        """
        Solve the CSP using backtracking with constraint propagation and a timeout.
        
        Args:
            timeout: Maximum time in seconds to spend on solving
        """
        print("\n[DEBUG] Starting solver with timeout", timeout, "seconds")
        
        # Initialize current domains for forward checking
        self.current_domains = {var: list(self.domains[var]) for var in self.variables}
        
        # Apply initial constraint propagation
        print("\n[DEBUG] Applying initial constraint propagation...")
        if not self._initial_constraint_propagation():
            print("[DEBUG] No solution exists (detected during initial constraint propagation)")
            return False
        
        print("\n[DEBUG] Board after initial constraint propagation:")
        self._print_debug_board()
        
        start_time = time.time()
        result = self._backtrack_with_constraint_propagation(start_time, timeout)
        end_time = time.time()
        
        print(f"\n[DEBUG] Nodes explored: {self.nodes_explored}")
        
        if result:
            print(f"Solution found in {end_time - start_time:.4f} seconds")
            return True
        else:
            if end_time - start_time >= timeout:
                print(f"Timeout after {timeout} seconds")
            else:
                print("No solution exists")
            return False
    
    def _initial_constraint_propagation(self) -> bool:
        """
        Apply initial constraint propagation before starting the search.
        Return False if inconsistency is detected.
        """
        # Create a working board with the initial values
        # Use Union type to allow both None and string values
        board: List[List[Optional[str]]] = [[None for _ in range(self.size)] for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] is not None:
                    board[i][j] = self.board[i][j]
        
        # Apply constraint propagation until no more changes
        iteration = 1
        changed = True
        while changed:
            print(f"\n[DEBUG] Constraint propagation iteration {iteration}")
            changed = False
            
            # Apply opportunity of elimination
            for i in range(self.size):
                for j in range(self.size):
                    if board[i][j] is None:
                        # Check row for two consecutive identical symbols
                        if j >= 2 and board[i][j-1] == board[i][j-2] and board[i][j-1] is not None:
                            # Must place the opposite symbol
                            opposite = '>' if board[i][j-1] == 'O' else 'O'
                            print(f"[DEBUG] Found two consecutive {board[i][j-1]} at ({i+1},{j-1}) and ({i+1},{j-2}), placing {opposite} at ({i+1},{j+1})")
                            board[i][j] = opposite
                            changed = True
                        elif j <= self.size-3 and board[i][j+1] == board[i][j+2] and board[i][j+1] is not None:
                            # Must place the opposite symbol
                            opposite = '>' if board[i][j+1] == 'O' else 'O'
                            print(f"[DEBUG] Found two consecutive {board[i][j+1]} at ({i+1},{j+2}) and ({i+1},{j+3}), placing {opposite} at ({i+1},{j+1})")
                            board[i][j] = opposite
                            changed = True
                        
                        # Check column for two consecutive identical symbols
                        if i >= 2 and board[i-1][j] == board[i-2][j] and board[i-1][j] is not None:
                            # Must place the opposite symbol
                            opposite = '>' if board[i-1][j] == 'O' else 'O'
                            print(f"[DEBUG] Found two consecutive {board[i-1][j]} at ({i},{j+1}) and ({i-1},{j+1}), placing {opposite} at ({i+1},{j+1})")
                            board[i][j] = opposite
                            changed = True
                        elif i <= self.size-3 and board[i+1][j] == board[i+2][j] and board[i+1][j] is not None:
                            # Must place the opposite symbol
                            opposite = '>' if board[i+1][j] == 'O' else 'O'
                            print(f"[DEBUG] Found two consecutive {board[i+1][j]} at ({i+2},{j+1}) and ({i+3},{j+1}), placing {opposite} at ({i+1},{j+1})")
                            board[i][j] = opposite
                            changed = True
            
            # Apply opportunity with constraints
            for i in range(self.size):
                for j in range(self.size):
                    if board[i][j] is not None:
                        # Check horizontal constraints
                        if j > 0 and j < self.size-1:
                            if (self.horizontal_constraints[i][j-1] == '=' and 
                                self.horizontal_constraints[i][j] == '=' and
                                board[i][j-1] is None and board[i][j+1] is None):
                                # Both adjacent cells must be the opposite to avoid three in a row
                                opposite = '>' if board[i][j] == 'O' else 'O'
                                print(f"[DEBUG] Found '=' constraints at ({i+1},{j}) and ({i+1},{j+1}) with {board[i][j]} at ({i+1},{j+1}), placing {opposite} at ({i+1},{j}) and ({i+1},{j+2})")
                                board[i][j-1] = opposite
                                board[i][j+1] = opposite
                                changed = True
                        
                        # Check vertical constraints
                        if i > 0 and i < self.size-1:
                            if (self.vertical_constraints[i-1][j] == '=' and 
                                self.vertical_constraints[i][j] == '=' and
                                board[i-1][j] is None and board[i+1][j] is None):
                                # Both adjacent cells must be the opposite to avoid three in a row
                                opposite = '>' if board[i][j] == 'O' else 'O'
                                print(f"[DEBUG] Found '=' constraints at ({i},{j+1}) and ({i+1},{j+1}) with {board[i][j]} at ({i+1},{j+1}), placing {opposite} at ({i},{j+1}) and ({i+2},{j+1})")
                                board[i-1][j] = opposite
                                board[i+1][j] = opposite
                                changed = True
            
            # Check for row/column balance (if a row/column has 3 of one symbol, the rest must be the other)
            for i in range(self.size):
                # Check rows
                row_o_count = sum(1 for j in range(self.size) if board[i][j] == 'O')
                row_gt_count = sum(1 for j in range(self.size) if board[i][j] == '>')
                
                if row_o_count == 3:
                    # Fill remaining cells with '>'
                    for j in range(self.size):
                        if board[i][j] is None:
                            print(f"[DEBUG] Row {i+1} already has 3 O's, placing > at ({i+1},{j+1})")
                            board[i][j] = '>'
                            changed = True
                
                if row_gt_count == 3:
                    # Fill remaining cells with 'O'
                    for j in range(self.size):
                        if board[i][j] is None:
                            print(f"[DEBUG] Row {i+1} already has 3 >'s, placing O at ({i+1},{j+1})")
                            board[i][j] = 'O'
                            changed = True
                
                # Check columns
                col_o_count = sum(1 for i2 in range(self.size) if board[i2][i] == 'O')
                col_gt_count = sum(1 for i2 in range(self.size) if board[i2][i] == '>')
                
                if col_o_count == 3:
                    # Fill remaining cells with '>'
                    for i2 in range(self.size):
                        if board[i2][i] is None:
                            print(f"[DEBUG] Column {i+1} already has 3 O's, placing > at ({i2+1},{i+1})")
                            board[i2][i] = '>'
                            changed = True
                
                if col_gt_count == 3:
                    # Fill remaining cells with 'O'
                    for i2 in range(self.size):
                        if board[i2][i] is None:
                            print(f"[DEBUG] Column {i+1} already has 3 >'s, placing O at ({i2+1},{i+1})")
                            board[i2][i] = 'O'
                            changed = True
            
            # Check for constraint violations
            for i in range(self.size):
                # Check rows
                row_values = [board[i][j] for j in range(self.size) if board[i][j] is not None]
                if not self._check_sequence(row_values):
                    print(f"[DEBUG] Row {i+1} has more than 2 consecutive identical symbols: {row_values}")
                    return False
                
                # Check columns
                col_values = [board[j][i] for j in range(self.size) if board[j][i] is not None]
                if not self._check_sequence(col_values):
                    print(f"[DEBUG] Column {i+1} has more than 2 consecutive identical symbols: {col_values}")
                    return False
            
            # Check horizontal constraints
            for i in range(self.size):
                for j in range(self.size-1):
                    constraint = self.horizontal_constraints[i][j]
                    if constraint != '.' and board[i][j] is not None and board[i][j+1] is not None:
                        if constraint == 'x' and board[i][j] == board[i][j+1]:
                            print(f"[DEBUG] Horizontal constraint 'x' violated at ({i+1},{j+1}): {board[i][j]} {constraint} {board[i][j+1]}")
                            return False
                        if constraint == '=' and board[i][j] != board[i][j+1]:
                            print(f"[DEBUG] Horizontal constraint '=' violated at ({i+1},{j+1}): {board[i][j]} {constraint} {board[i][j+1]}")
                            return False
            
            # Check vertical constraints
            for i in range(self.size-1):
                for j in range(self.size):
                    constraint = self.vertical_constraints[i][j]
                    if constraint != '.' and board[i][j] is not None and board[i+1][j] is not None:
                        if constraint == 'x' and board[i][j] == board[i+1][j]:
                            print(f"[DEBUG] Vertical constraint 'x' violated at ({i+1},{j+1}): {board[i][j]} {constraint} {board[i+1][j]}")
                            return False
                        if constraint == '=' and board[i][j] != board[i+1][j]:
                            print(f"[DEBUG] Vertical constraint '=' violated at ({i+1},{j+1}): {board[i][j]} {constraint} {board[i+1][j]}")
                            return False
            
            if changed:
                print("\n[DEBUG] Board after iteration", iteration)
                self._print_debug_board(board)
            
            iteration += 1
        
        # Update the board and assignment with the propagated values
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] is None and board[i][j] is not None:
                    self.board[i][j] = board[i][j]
                    if (i, j) in self.variables:
                        self.assignment[(i, j)] = board[i][j]
                        # Update current domains
                        self.current_domains[(i, j)] = [board[i][j]]
                        print(f"[DEBUG] Updated assignment: ({i+1},{j+1}) = {board[i][j]}")
        
        return True
    
    def _backtrack_with_constraint_propagation(self, start_time, timeout) -> bool:
        """Backtracking algorithm with constraint propagation to find a solution"""
        self.debug_depth += 1
        indent = "  " * self.debug_depth
        self.nodes_explored += 1
        
        # Check timeout
        if time.time() - start_time >= timeout:
            print(f"{indent}[DEBUG] Timeout reached")
            self.debug_depth -= 1
            return False
        
        if self.is_complete():
            print(f"{indent}[DEBUG] Solution found!")
            self.debug_depth -= 1
            return True
        
        var = self.select_unassigned_variable()
        row, col = var
        print(f"\n{indent}[DEBUG] Selected variable: ({row+1},{col+1})")
        print(f"{indent}[DEBUG] Current board state:")
        self._print_debug_board(indent=indent)
        
        domain_values = self.order_domain_values(var)
        print(f"{indent}[DEBUG] Ordered domain values: {domain_values}")
        
        for value in domain_values:
            print(f"\n{indent}[DEBUG] Trying {value} at ({row+1},{col+1})")
            
            if self.is_consistent(var, value):
                print(f"{indent}[DEBUG] {value} is consistent at ({row+1},{col+1})")
                
                # Assign value to var
                self.assignment[var] = value
                self.board[row][col] = value
                
                # Save current domains and board state
                saved_domains = {v: list(self.current_domains[v]) for v in self.variables if v != var}
                saved_board = copy.deepcopy(self.board)
                
                # Apply constraint propagation
                print(f"{indent}[DEBUG] Applying constraint propagation after assigning {value} to ({row+1},{col+1})")
                if self._constraint_propagation():
                    # Recursively try to complete the assignment
                    if self._backtrack_with_constraint_propagation(start_time, timeout):
                        self.debug_depth -= 1
                        return True
                else:
                    print(f"{indent}[DEBUG] Constraint propagation failed after assigning {value} to ({row+1},{col+1})")
                
                # If we get here, this assignment didn't work
                print(f"{indent}[DEBUG] Backtracking from {value} at ({row+1},{col+1})")
                del self.assignment[var]
                
                # Restore domains and board
                for v in saved_domains:
                    self.current_domains[v] = saved_domains[v]
                self.board = saved_board
            else:
                print(f"{indent}[DEBUG] {value} is NOT consistent at ({row+1},{col+1})")
                self._explain_inconsistency(var, value)
        
        print(f"{indent}[DEBUG] No valid value found for ({row+1},{col+1})")
        self.debug_depth -= 1
        return False
    
    def _explain_inconsistency(self, var, value):
        """Explain why a value is inconsistent for a variable"""
        row, col = var
        indent = "  " * self.debug_depth
        
        # Create a temporary board with the current assignment and the new value
        # Use Union type to allow both None and string values
        temp_board: List[List[Optional[str]]] = [[None for _ in range(self.size)] for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] is not None:
                    temp_board[i][j] = self.board[i][j]
        
        for (r, c), v in self.assignment.items():
            temp_board[r][c] = v
        temp_board[row][col] = value
        
        # Check row constraints
        row_values = [temp_board[row][c] for c in range(self.size) if temp_board[row][c] is not None]
        if not self._check_sequence(row_values):
            print(f"{indent}[DEBUG] Reason: Would create more than 2 consecutive identical symbols in row {row+1}")
            return
        
        # Count symbols in the row
        row_o_count = sum(1 for c in range(self.size) if temp_board[row][c] == 'O')
        row_gt_count = sum(1 for c in range(self.size) if temp_board[row][c] == '>')
        
        # Check if we've exceeded the maximum allowed symbols per row
        if row_o_count > 3:
            print(f"{indent}[DEBUG] Reason: Row {row+1} would have more than 3 O's ({row_o_count})")
            return
        if row_gt_count > 3:
            print(f"{indent}[DEBUG] Reason: Row {row+1} would have more than 3 >'s ({row_gt_count})")
            return
        
        # Check if we've filled the row and have the correct counts
        if row_o_count + row_gt_count == self.size and (row_o_count != 3 or row_gt_count != 3):
            print(f"{indent}[DEBUG] Reason: Row {row+1} would have {row_o_count} O's and {row_gt_count} >'s (should be 3 each)")
            return
        
        # Check column constraints
        col_values = [temp_board[r][col] for r in range(self.size) if temp_board[r][col] is not None]
        if not self._check_sequence(col_values):
            print(f"{indent}[DEBUG] Reason: Would create more than 2 consecutive identical symbols in column {col+1}")
            return
        
        # Count symbols in the column
        col_o_count = sum(1 for r in range(self.size) if temp_board[r][col] == 'O')
        col_gt_count = sum(1 for r in range(self.size) if temp_board[r][col] == '>')
        
        # Check if we've exceeded the maximum allowed symbols per column
        if col_o_count > 3:
            print(f"{indent}[DEBUG] Reason: Column {col+1} would have more than 3 O's ({col_o_count})")
            return
        if col_gt_count > 3:
            print(f"{indent}[DEBUG] Reason: Column {col+1} would have more than 3 >'s ({col_gt_count})")
            return
        
        # Check if we've filled the column and have the correct counts
        if col_o_count + col_gt_count == self.size and (col_o_count != 3 or col_gt_count != 3):
            print(f"{indent}[DEBUG] Reason: Column {col+1} would have {col_o_count} O's and {col_gt_count} >'s (should be 3 each)")
            return
        
        # Check horizontal constraints between cells
        if col > 0:
            left_cell = temp_board[row][col-1]
            constraint = self.horizontal_constraints[row][col-1]
            if left_cell is not None:
                if constraint == 'x' and left_cell == value:
                    print(f"{indent}[DEBUG] Reason: Would violate horizontal constraint 'x' with ({row+1},{col})")
                    return
                if constraint == '=' and left_cell != value:
                    print(f"{indent}[DEBUG] Reason: Would violate horizontal constraint '=' with ({row+1},{col})")
                    return
        
        if col < self.size - 1:
            right_cell = temp_board[row][col+1]
            constraint = self.horizontal_constraints[row][col]
            if right_cell is not None:
                if constraint == 'x' and right_cell == value:
                    print(f"{indent}[DEBUG] Reason: Would violate horizontal constraint 'x' with ({row+1},{col+2})")
                    return
                if constraint == '=' and right_cell != value:
                    print(f"{indent}[DEBUG] Reason: Would violate horizontal constraint '=' with ({row+1},{col+2})")
                    return
        
        # Check vertical constraints between cells
        if row > 0:
            above_cell = temp_board[row-1][col]
            constraint = self.vertical_constraints[row-1][col]
            if above_cell is not None:
                if constraint == 'x' and above_cell == value:
                    print(f"{indent}[DEBUG] Reason: Would violate vertical constraint 'x' with ({row},{col+1})")
                    return
                if constraint == '=' and above_cell != value:
                    print(f"{indent}[DEBUG] Reason: Would violate vertical constraint '=' with ({row},{col+1})")
                    return
        
        if row < self.size - 1:
            below_cell = temp_board[row+1][col]
            constraint = self.vertical_constraints[row][col]
            if below_cell is not None:
                if constraint == 'x' and below_cell == value:
                    print(f"{indent}[DEBUG] Reason: Would violate vertical constraint 'x' with ({row+2},{col+1})")
                    return
                if constraint == '=' and below_cell != value:
                    print(f"{indent}[DEBUG] Reason: Would violate vertical constraint '=' with ({row+2},{col+1})")
                    return
        
        print(f"{indent}[DEBUG] Reason: Unknown inconsistency")
    
    def _constraint_propagation(self) -> bool:
        """
        Apply constraint propagation after each assignment.
        Return False if inconsistency is detected.
        """
        indent = "  " * self.debug_depth
        
        # Create a working board with the current assignment
        # Use Union type to allow both None and string values
        board: List[List[Optional[str]]] = [[None for _ in range(self.size)] for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] is not None:
                    board[i][j] = self.board[i][j]
        
        # Apply constraint propagation until no more changes
        iteration = 1
        changed = True
        while changed:
            print(f"{indent}[DEBUG] Constraint propagation iteration {iteration}")
            changed = False
            
            # Apply opportunity of elimination
            for i in range(self.size):
                for j in range(self.size):
                    if board[i][j] is None:
                        # Check row for two consecutive identical symbols
                        if j >= 2 and board[i][j-1] == board[i][j-2] and board[i][j-1] is not None:
                            # Must place the opposite symbol
                            opposite = '>' if board[i][j-1] == 'O' else 'O'
                            print(f"{indent}[DEBUG] Found two consecutive {board[i][j-1]} at ({i+1},{j-1}) and ({i+1},{j-2}), placing {opposite} at ({i+1},{j+1})")
                            board[i][j] = opposite
                            changed = True
                        elif j <= self.size-3 and board[i][j+1] == board[i][j+2] and board[i][j+1] is not None:
                            # Must place the opposite symbol
                            opposite = '>' if board[i][j+1] == 'O' else 'O'
                            print(f"{indent}[DEBUG] Found two consecutive {board[i][j+1]} at ({i+1},{j+2}) and ({i+1},{j+3}), placing {opposite} at ({i+1},{j+1})")
                            board[i][j] = opposite
                            changed = True
                        
                        # Check column for two consecutive identical symbols
                        if i >= 2 and board[i-1][j] == board[i-2][j] and board[i-1][j] is not None:
                            # Must place the opposite symbol
                            opposite = '>' if board[i-1][j] == 'O' else 'O'
                            print(f"{indent}[DEBUG] Found two consecutive {board[i-1][j]} at ({i},{j+1}) and ({i-1},{j+1}), placing {opposite} at ({i+1},{j+1})")
                            board[i][j] = opposite
                            changed = True
                        elif i <= self.size-3 and board[i+1][j] == board[i+2][j] and board[i+1][j] is not None:
                            # Must place the opposite symbol
                            opposite = '>' if board[i+1][j] == 'O' else 'O'
                            print(f"{indent}[DEBUG] Found two consecutive {board[i+1][j]} at ({i+2},{j+1}) and ({i+3},{j+1}), placing {opposite} at ({i+1},{j+1})")
                            board[i][j] = opposite
                            changed = True
            
            # Check for constraint violations
            for i in range(self.size):
                # Check rows
                row_values = [board[i][j] for j in range(self.size) if board[i][j] is not None]
                if not self._check_sequence(row_values):
                    print(f"{indent}[DEBUG] Row {i+1} has more than 2 consecutive identical symbols: {row_values}")
                    return False
                
                # Check columns
                col_values = [board[j][i] for j in range(self.size) if board[j][i] is not None]
                if not self._check_sequence(col_values):
                    print(f"{indent}[DEBUG] Column {i+1} has more than 2 consecutive identical symbols: {col_values}")
                    return False
            
            if changed:
                print(f"{indent}[DEBUG] Board after iteration {iteration}")
                self._print_debug_board(board, indent)
            
            iteration += 1
        
        # Update the board and assignment with the propagated values
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] is None and board[i][j] is not None:
                    self.board[i][j] = board[i][j]
                    if (i, j) in self.variables:
                        self.assignment[(i, j)] = board[i][j]
                        # Update current domains
                        self.current_domains[(i, j)] = [board[i][j]]
                        print(f"{indent}[DEBUG] Updated assignment: ({i+1},{j+1}) = {board[i][j]}")
        
        return True
    
    def _print_debug_board(self, board=None, indent=""):
        """Print the current state of the board for debugging"""
        if board is None:
            board = self.board
        
        for i in range(self.size):
            row_str = indent
            for j in range(self.size):
                cell = board[i][j]
                if cell is None:
                    row_str += ". "
                else:
                    row_str += cell + " "
            print(row_str)

def main():
    print("Debug Enhanced Binary Puzzle Solver")
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
    
    print("Initial board:")
    for row in initial_board:
        print(' '.join(cell if cell is not None else '.' for cell in row))
    
    print("\nHorizontal constraints:")
    for row in horizontal_constraints:
        print(' '.join(row))
    
    print("\nVertical constraints:")
    for row in vertical_constraints:
        print(' '.join(row))
    
    print("\nSolving with debug output...")
    puzzle = DebugEnhancedBinaryPuzzleCSP(horizontal_constraints, vertical_constraints, initial_board)
    if puzzle.solve(timeout=30):
        solution = puzzle.get_solution_board()
        print("\nSolution:")
        for row in solution:
            print(' '.join(str(cell) for cell in row))
    else:
        print("No solution found")

if __name__ == "__main__":
    main()