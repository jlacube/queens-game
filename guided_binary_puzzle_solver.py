"""
Guided Binary Puzzle Solver that uses the user's solution as a guide
"""

from binary_puzzle_csp import BinaryPuzzleCSP
import time
import copy
from typing import List, Dict, Tuple, Optional, Any, Union

class GuidedBinaryPuzzleCSP(BinaryPuzzleCSP):
    """
    Guided Binary Puzzle CSP that uses the user's solution as a guide
    """
    
    def __init__(self, horizontal_constraints=None, vertical_constraints=None, initial_board=None, guide_solution=None):
        """
        Initialize with a guide solution to help direct the search
        """
        super().__init__(horizontal_constraints, vertical_constraints, initial_board)
        self.guide_solution = guide_solution
        self.debug_level = 1  # 0: no debug, 1: basic, 2: detailed
    
    def solve(self, timeout=30) -> bool:
        """
        Solve the CSP using the guide solution and a timeout.
        
        Args:
            timeout: Maximum time in seconds to spend on solving
        """
        # Initialize current domains for forward checking
        self.current_domains = {var: list(self.domains[var]) for var in self.variables}
        
        # Apply initial constraint propagation
        if not self._initial_constraint_propagation():
            print("No solution exists (detected during initial constraint propagation)")
            return False
        
        start_time = time.time()
        result = self._guided_backtrack(start_time, timeout)
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
    
    def _initial_constraint_propagation(self) -> bool:
        """
        Apply initial constraint propagation before starting the search.
        Return False if inconsistency is detected.
        """
        if self.debug_level >= 1:
            print("Applying initial constraint propagation...")
        
        # Create a working board with the initial values
        board: List[List[Optional[str]]] = [[None for _ in range(self.size)] for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] is not None:
                    board[i][j] = self.board[i][j]
        
        # Apply constraint propagation until no more changes
        changed = True
        iteration = 0
        while changed:
            iteration += 1
            if self.debug_level >= 2:
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
            for i in range(self.size):
                # Check rows
                row_values = [board[i][j] for j in range(self.size) if board[i][j] is not None]
                if not self._check_sequence(row_values):
                    if self.debug_level >= 1:
                        print(f"Row {i+1} has more than 2 consecutive identical symbols")
                    return False
                
                # Check columns
                col_values = [board[j][i] for j in range(self.size) if board[j][i] is not None]
                if not self._check_sequence(col_values):
                    if self.debug_level >= 1:
                        print(f"Column {i+1} has more than 2 consecutive identical symbols")
                    return False
            
            # Check horizontal constraints
            for i in range(self.size):
                for j in range(self.size-1):
                    constraint = self.horizontal_constraints[i][j]
                    if constraint != '.' and board[i][j] is not None and board[i][j+1] is not None:
                        if constraint == 'x' and board[i][j] == board[i][j+1]:
                            if self.debug_level >= 1:
                                print(f"Horizontal constraint 'x' violated at ({i+1},{j+1})")
                            return False
                        if constraint == '=' and board[i][j] != board[i][j+1]:
                            if self.debug_level >= 1:
                                print(f"Horizontal constraint '=' violated at ({i+1},{j+1})")
                            return False
            
            # Check vertical constraints
            for i in range(self.size-1):
                for j in range(self.size):
                    constraint = self.vertical_constraints[i][j]
                    if constraint != '.' and board[i][j] is not None and board[i+1][j] is not None:
                        if constraint == 'x' and board[i][j] == board[i+1][j]:
                            if self.debug_level >= 1:
                                print(f"Vertical constraint 'x' violated at ({i+1},{j+1})")
                            return False
                        if constraint == '=' and board[i][j] != board[i+1][j]:
                            if self.debug_level >= 1:
                                print(f"Vertical constraint '=' violated at ({i+1},{j+1})")
                            return False
            
            if changed and self.debug_level >= 2:
                print("\nBoard after iteration", iteration)
                self._print_debug_board(board)
        
        # Update the board and assignment with the propagated values
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] is None and board[i][j] is not None:
                    self.board[i][j] = board[i][j]
                    if (i, j) in self.variables:
                        self.assignment[(i, j)] = board[i][j]
                        # Update current domains
                        self.current_domains[(i, j)] = [board[i][j]]
                        if self.debug_level >= 2:
                            print(f"Updated assignment: ({i+1},{j+1}) = {board[i][j]}")
        
        return True
    
    def _guided_backtrack(self, start_time, timeout) -> bool:
        """
        Backtracking algorithm guided by the user's solution
        """
        # Check timeout
        if time.time() - start_time >= timeout:
            return False
        
        if self.is_complete():
            return True
        
        # Select variable based on the guide solution
        var = self._select_guided_variable()
        
        if var is None:
            # Fall back to regular variable selection
            var = self.select_unassigned_variable()
        
        if self.debug_level >= 2:
            print(f"Selected variable: ({var[0]+1},{var[1]+1})")
        
        # Get the guide value for this variable
        guide_value = None
        if self.guide_solution is not None:
            guide_value = self.guide_solution[var[0]][var[1]]
        
        # Try the guide value first, then the other value
        domain_values = self.current_domains[var].copy()
        if guide_value in domain_values:
            # Move the guide value to the front
            domain_values.remove(guide_value)
            domain_values.insert(0, guide_value)
        
        for value in domain_values:
            if self.debug_level >= 2:
                print(f"Trying {value} at ({var[0]+1},{var[1]+1})")
            
            if self.is_consistent(var, value):
                if self.debug_level >= 2:
                    print(f"{value} is consistent at ({var[0]+1},{var[1]+1})")
                
                # Assign value to var
                self.assignment[var] = value
                self.board[var[0]][var[1]] = value
                
                # Save current domains and board state
                saved_domains = {v: list(self.current_domains[v]) for v in self.variables if v != var}
                saved_board = copy.deepcopy(self.board)
                
                # Update domains of unassigned variables
                for other_var in self.variables:
                    if other_var != var and other_var not in self.assignment:
                        self.current_domains[other_var] = [
                            val for val in self.current_domains[other_var]
                            if self._is_consistent_for_neighbor(other_var, val, self.board)
                        ]
                        if not self.current_domains[other_var]:
                            # Domain wipeout, backtrack
                            if self.debug_level >= 2:
                                print(f"Domain wipeout for ({other_var[0]+1},{other_var[1]+1})")
                            self.assignment.pop(var)
                            for v in saved_domains:
                                self.current_domains[v] = saved_domains[v]
                            self.board = saved_board
                            break
                else:
                    # No domain wipeout, continue with backtracking
                    if self._guided_backtrack(start_time, timeout):
                        return True
                
                # If we get here, this assignment didn't work
                if var in self.assignment:
                    if self.debug_level >= 2:
                        print(f"Backtracking from {value} at ({var[0]+1},{var[1]+1})")
                    self.assignment.pop(var)
                
                # Restore domains and board
                for v in saved_domains:
                    self.current_domains[v] = saved_domains[v]
                self.board = saved_board
            else:
                if self.debug_level >= 2:
                    print(f"{value} is NOT consistent at ({var[0]+1},{var[1]+1})")
        
        if self.debug_level >= 2:
            print(f"No valid value found for ({var[0]+1},{var[1]+1})")
        return False
    
    def _select_guided_variable(self):
        """
        Select an unassigned variable based on the guide solution.
        Prefer variables where the guide solution has a value that is consistent.
        """
        if self.guide_solution is None:
            return None
        
        unassigned = [v for v in self.variables if v not in self.assignment]
        if not unassigned:
            return None
        
        # First, try to find a variable where the guide value is consistent
        for var in unassigned:
            row, col = var
            guide_value = self.guide_solution[row][col]
            if guide_value in self.current_domains[var] and self.is_consistent(var, guide_value):
                return var
        
        # If no such variable exists, use MRV heuristic
        return self.select_unassigned_variable()
    
    def _print_debug_board(self, board=None):
        """Print the current state of the board for debugging"""
        if board is None:
            board = self.board
        
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
    print("Guided Binary Puzzle Solver")
    print("==========================\n")
    
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
    
    print("\nSolving with guided approach...")
    puzzle = GuidedBinaryPuzzleCSP(horizontal_constraints, vertical_constraints, initial_board, user_solution)
    if puzzle.solve(timeout=30):
        solution = puzzle.get_solution_board()
        print("\nSolution:")
        for row in solution:
            print(' '.join(str(cell) for cell in row))
        
        # Verify the solution
        print("\nVerifying solution...")
        
        # Check rows
        for i in range(6):
            row = solution[i]
            o_count = sum(1 for cell in row if cell == 'O')
            gt_count = sum(1 for cell in row if cell == '>')
            print(f"Row {i+1}: {o_count} O's, {gt_count} >'s - ", end="")
            print("✓" if o_count == 3 and gt_count == 3 else "✗")
        
        # Check columns
        for j in range(6):
            col = [solution[i][j] for i in range(6)]
            o_count = sum(1 for cell in col if cell == 'O')
            gt_count = sum(1 for cell in col if cell == '>')
            print(f"Column {j+1}: {o_count} O's, {gt_count} >'s - ", end="")
            print("✓" if o_count == 3 and gt_count == 3 else "✗")
        
        # Check for more than 2 consecutive identical symbols
        valid_sequence = True
        for i in range(6):
            # Check rows
            row = solution[i]
            for j in range(2, 6):
                if row[j] == row[j-1] == row[j-2]:
                    valid_sequence = False
                    print(f"Error: 3 consecutive {row[j]} in row {i+1} at positions {j-2+1}, {j-1+1}, {j+1}")
            
            # Check columns
            col = [solution[r][i] for r in range(6)]
            for j in range(2, 6):
                if col[j] == col[j-1] == col[j-2]:
                    valid_sequence = False
                    print(f"Error: 3 consecutive {col[j]} in column {i+1} at positions {j-2+1}, {j-1+1}, {j+1}")
        
        if valid_sequence:
            print("No more than 2 consecutive identical symbols: ✓")
        else:
            print("There are more than 2 consecutive identical symbols: ✗")
        
        # Check horizontal constraints
        valid_h_constraints = True
        for i in range(6):
            for j in range(5):
                constraint = horizontal_constraints[i][j]
                if constraint != '.':
                    left = solution[i][j]
                    right = solution[i][j+1]
                    if constraint == 'x' and left == right:
                        valid_h_constraints = False
                        print(f"Error: Horizontal constraint 'x' violated at ({i+1},{j+1}): {left} {constraint} {right}")
                    elif constraint == '=' and left != right:
                        valid_h_constraints = False
                        print(f"Error: Horizontal constraint '=' violated at ({i+1},{j+1}): {left} {constraint} {right}")
        
        if valid_h_constraints:
            print("All horizontal constraints are satisfied: ✓")
        else:
            print("Not all horizontal constraints are satisfied: ✗")
        
        # Check vertical constraints
        valid_v_constraints = True
        for i in range(5):
            for j in range(6):
                constraint = vertical_constraints[i][j]
                if constraint != '.':
                    top = solution[i][j]
                    bottom = solution[i+1][j]
                    if constraint == 'x' and top == bottom:
                        valid_v_constraints = False
                        print(f"Error: Vertical constraint 'x' violated at ({i+1},{j+1}): {top} {constraint} {bottom}")
                    elif constraint == '=' and top != bottom:
                        valid_v_constraints = False
                        print(f"Error: Vertical constraint '=' violated at ({i+1},{j+1}): {top} {constraint} {bottom}")
        
        if valid_v_constraints:
            print("All vertical constraints are satisfied: ✓")
        else:
            print("Not all vertical constraints are satisfied: ✗")
        
        # Compare with user's solution
        matches_user = True
        for i in range(6):
            for j in range(6):
                if solution[i][j] != user_solution[i][j]:
                    matches_user = False
                    print(f"Mismatch at ({i+1},{j+1}): Found {solution[i][j]}, expected {user_solution[i][j]}")
        
        if matches_user:
            print("\nThe solution matches the user's solution! ✓")
        else:
            print("\nThe solution differs from the user's solution, but may still be valid.")
        
        # Overall verdict
        if (valid_sequence and valid_h_constraints and valid_v_constraints):
            print("\nThe solution is VALID! ✓")
        else:
            print("\nThe solution is INVALID! ✗")
    else:
        print("No solution found")

if __name__ == "__main__":
    main()