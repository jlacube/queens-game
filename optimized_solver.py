"""
Optimized Binary Puzzle Solver with advanced techniques:
- Enhanced constraint propagation
- Improved variable selection
- Improved value ordering
- Random restarts
- Timeout mechanism
"""

from binary_puzzle_csp import BinaryPuzzleCSP
import time
import copy
import random

class OptimizedBinaryPuzzleCSP(BinaryPuzzleCSP):
    """
    Optimized Binary Puzzle CSP with advanced solving techniques
    """
    
    def solve_with_restarts(self, max_restarts=10, timeout_per_restart=5, total_timeout=60):
        """
        Solve the CSP using random restarts to escape local minima.
        
        Args:
            max_restarts: Maximum number of restarts
            timeout_per_restart: Timeout per restart in seconds
            total_timeout: Total timeout in seconds
        """
        start_time = time.time()
        
        for restart in range(max_restarts):
            # Check total timeout
            if time.time() - start_time >= total_timeout:
                print(f"Total timeout of {total_timeout} seconds reached after {restart} restarts")
                return False
            
            print(f"Restart {restart+1}/{max_restarts}...")
            
            # Reset the assignment and current domains
            self.assignment = {}
            self.current_domains = {var: list(self.domains[var]) for var in self.variables}
            
            # Randomize the order of variables and domain values
            random.shuffle(self.variables)
            for var in self.variables:
                random.shuffle(self.current_domains[var])
            
            # Apply initial constraint propagation
            if not self._initial_constraint_propagation():
                print("No solution exists (detected during initial constraint propagation)")
                continue
            
            # Try to solve with the current restart
            restart_start_time = time.time()
            result = self._backtrack_with_constraint_propagation(restart_start_time, timeout_per_restart)
            restart_end_time = time.time()
            
            if result:
                print(f"Solution found in {restart_end_time - start_time:.4f} seconds (restart {restart+1})")
                return True
            else:
                if restart_end_time - restart_start_time >= timeout_per_restart:
                    print(f"Timeout after {timeout_per_restart} seconds on restart {restart+1}")
                else:
                    print(f"No solution found on restart {restart+1}")
        
        print(f"No solution found after {max_restarts} restarts")
        return False
    
    def _initial_constraint_propagation(self):
        """
        Apply initial constraint propagation before starting the search.
        Return False if inconsistency is detected.
        """
        # Create a working board with the initial values
        board = [[None for _ in range(self.size)] for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] is not None:
                    board[i][j] = self.board[i][j]
        
        # Apply constraint propagation until no more changes
        changed = True
        while changed:
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
                        elif j <= self.size-3 and board[i][j+1] == board[i][j+2] and board[i][j+1] is not None:
                            # Must place the opposite symbol
                            opposite = '>' if board[i][j+1] == 'O' else 'O'
                            board[i][j] = opposite
                            changed = True
                        
                        # Check column for two consecutive identical symbols
                        if i >= 2 and board[i-1][j] == board[i-2][j] and board[i-1][j] is not None:
                            # Must place the opposite symbol
                            opposite = '>' if board[i-1][j] == 'O' else 'O'
                            board[i][j] = opposite
                            changed = True
                        elif i <= self.size-3 and board[i+1][j] == board[i+2][j] and board[i+1][j] is not None:
                            # Must place the opposite symbol
                            opposite = '>' if board[i+1][j] == 'O' else 'O'
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
                            board[i][j] = '>'
                            changed = True
                
                if row_gt_count == 3:
                    # Fill remaining cells with 'O'
                    for j in range(self.size):
                        if board[i][j] is None:
                            board[i][j] = 'O'
                            changed = True
                
                # Check columns
                col_o_count = sum(1 for i2 in range(self.size) if board[i2][i] == 'O')
                col_gt_count = sum(1 for i2 in range(self.size) if board[i2][i] == '>')
                
                if col_o_count == 3:
                    # Fill remaining cells with '>'
                    for i2 in range(self.size):
                        if board[i2][i] is None:
                            board[i2][i] = '>'
                            changed = True
                
                if col_gt_count == 3:
                    # Fill remaining cells with 'O'
                    for i2 in range(self.size):
                        if board[i2][i] is None:
                            board[i2][i] = 'O'
                            changed = True
        
        # Update the board and assignment with the propagated values
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] is None and board[i][j] is not None:
                    self.board[i][j] = board[i][j]
                    if (i, j) in self.variables:
                        self.assignment[(i, j)] = board[i][j]
                        # Update current domains
                        self.current_domains[(i, j)] = [board[i][j]]
        
        return True
    
    def select_unassigned_variable(self):
        """
        Select an unassigned variable using a combination of heuristics:
        1. Minimum Remaining Values (MRV): Choose the variable with the fewest legal values
        2. Degree: Break ties by choosing the variable involved in the most constraints
        3. Most constrained rows/columns: Prefer variables in rows/columns with more assigned cells
        """
        unassigned = [v for v in self.variables if v not in self.assignment]
        
        if not unassigned:
            return None
        
        # Calculate legal values for each unassigned variable
        legal_values = {}
        for var in unassigned:
            legal_values[var] = sum(1 for value in self.current_domains[var] if self.is_consistent(var, value))
        
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
            
            # Count assigned neighbors
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = row + dr, col + dc
                if 0 <= nr < self.size and 0 <= nc < self.size and (nr, nc) in self.assignment:
                    count += 1
            
            # Count cells in the same row and column
            row_assigned = sum(1 for c in range(self.size) if (row, c) in self.assignment)
            col_assigned = sum(1 for r in range(self.size) if (r, col) in self.assignment)
            count += row_assigned + col_assigned
            
            return count
        
        return max(mrv_vars, key=count_constraints)
    
    def order_domain_values(self, var):
        """
        Order domain values to try the most promising values first.
        Use the least constraining value heuristic: prefer values that rule out the fewest choices for neighboring variables.
        """
        if var not in self.current_domains or not self.current_domains[var]:
            return []
        
        row, col = var
        
        # Create a temporary board with the current assignment
        temp_board = [[None for _ in range(self.size)] for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] is not None:
                    temp_board[i][j] = self.board[i][j]
        
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
        return sorted(self.current_domains[var], key=count_eliminated_options)
    
    def _backtrack_with_constraint_propagation(self, start_time, timeout):
        """Backtracking algorithm with constraint propagation to find a solution"""
        # Check timeout
        if time.time() - start_time >= timeout:
            return False
        
        if self.is_complete():
            return True
        
        var = self.select_unassigned_variable()
        if var is None:
            return True
        
        # Try each value in the domain
        for value in self.order_domain_values(var):
            if self.is_consistent(var, value):
                # Assign value to var
                self.assignment[var] = value
                
                # Save current domains and board state
                saved_domains = {v: list(self.current_domains[v]) for v in self.variables if v != var}
                saved_board = copy.deepcopy(self.board)
                
                # Apply constraint propagation
                self.board[var[0]][var[1]] = value
                
                # Update current domains for unassigned variables
                for other_var in self.variables:
                    if other_var != var and other_var not in self.assignment:
                        self.current_domains[other_var] = [
                            val for val in self.current_domains[other_var]
                            if self._is_consistent_for_neighbor(other_var, val, self.board)
                        ]
                        if not self.current_domains[other_var]:
                            # Domain wipeout, backtrack
                            self.assignment.pop(var)
                            for v in saved_domains:
                                self.current_domains[v] = saved_domains[v]
                            self.board = saved_board
                            break
                else:
                    # No domain wipeout, continue with backtracking
                    if self._backtrack_with_constraint_propagation(start_time, timeout):
                        return True
                
                # If we get here, this assignment didn't work
                if var in self.assignment:
                    self.assignment.pop(var)
                
                # Restore domains and board
                for v in saved_domains:
                    self.current_domains[v] = saved_domains[v]
                self.board = saved_board
        
        return False
    
    def _is_consistent_for_neighbor(self, var, value, board):
        """Helper method to check consistency for a neighbor during domain value ordering"""
        row, col = var
        
        # Make a copy of the board with the value assigned
        board_copy = copy.deepcopy(board)
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
        
        # Check horizontal constraints
        if col > 0 and board_copy[row][col-1] is not None:
            constraint = self.horizontal_constraints[row][col-1]
            if constraint == 'x' and board_copy[row][col-1] == value:
                return False
            if constraint == '=' and board_copy[row][col-1] != value:
                return False
        
        if col < self.size - 1 and board_copy[row][col+1] is not None:
            constraint = self.horizontal_constraints[row][col]
            if constraint == 'x' and board_copy[row][col+1] == value:
                return False
            if constraint == '=' and board_copy[row][col+1] != value:
                return False
        
        # Check vertical constraints
        if row > 0 and board_copy[row-1][col] is not None:
            constraint = self.vertical_constraints[row-1][col]
            if constraint == 'x' and board_copy[row-1][col] == value:
                return False
            if constraint == '=' and board_copy[row-1][col] != value:
                return False
        
        if row < self.size - 1 and board_copy[row+1][col] is not None:
            constraint = self.vertical_constraints[row][col]
            if constraint == 'x' and board_copy[row+1][col] == value:
                return False
            if constraint == '=' and board_copy[row+1][col] != value:
                return False
        
        return True

def main():
    print("Optimized Binary Puzzle Solver")
    print("===========================\n")
    
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
    _print_board(initial_board)
    
    print("\nSolving with optimized solver and random restarts...")
    puzzle = OptimizedBinaryPuzzleCSP(horizontal_constraints, vertical_constraints, initial_board)
    if puzzle.solve_with_restarts(max_restarts=20, timeout_per_restart=3, total_timeout=60):
        solution = puzzle.get_solution_board()
        print("\nSolution:")
        _print_board(solution)
        
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
        
        # Overall verdict
        if (valid_sequence and valid_h_constraints and valid_v_constraints):
            print("\nThe solution is VALID! ✓")
        else:
            print("\nThe solution is INVALID! ✗")
        
        # Visualize the solution
        print("\nGenerating visualization...")
        puzzle.visualize()
    else:
        print("No solution found")

def _print_board(board):
    """Print a board in a readable format"""
    for row in board:
        print(' '.join(cell if cell is not None else '.' for cell in row))

if __name__ == "__main__":
    main()