"""
Complete Fixed Binary Puzzle Solver with corrected sequence checking
"""

from binary_puzzle_csp import BinaryPuzzleCSP
import time
import copy
import random
from typing import List, Dict, Tuple, Optional, Any, Union

class FixedBinaryPuzzleCSP(BinaryPuzzleCSP):
    """
    Fixed Binary Puzzle CSP with corrected _check_sequence method and improved solving strategies
    """
    
    def __init__(self, horizontal_constraints=None, vertical_constraints=None, initial_board=None):
        """Initialize with improved settings"""
        super().__init__(horizontal_constraints, vertical_constraints, initial_board)
        self.debug_level = 0  # 0: no debug, 1: basic, 2: detailed
        self.nodes_explored = 0
        self.max_nodes = 100000  # Limit nodes to explore before restarting
    
    def _check_sequence(self, values):
        """
        FIXED: Check if a sequence of values has no more than 2 consecutive identical symbols.
        This version properly handles None values by only considering consecutive positions.
        
        Args:
            values: List of values ('O', '>', or None)
        """
        # Don't filter out None values, but track consecutive positions
        consecutive_count = 1
        last_symbol = None
        
        for value in values:
            if value is None:
                # None values break consecutive sequences
                consecutive_count = 1
                last_symbol = None
                continue
                
            if last_symbol is None:
                # First non-None value in a sequence
                last_symbol = value
                consecutive_count = 1
            elif value == last_symbol:
                # Same symbol as previous
                consecutive_count += 1
                if consecutive_count > 2:
                    return False
            else:
                # Different symbol
                last_symbol = value
                consecutive_count = 1
                
        return True
    
    def solve_with_restarts(self, max_restarts=20, timeout_per_restart=5, total_timeout=60):
        """
        Solve the CSP using random restarts with different variable orderings
        
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
            self.nodes_explored = 0
            
            # Use different variable ordering strategies for different restarts
            strategy = restart % 4
            if strategy == 0:
                # Standard MRV + degree
                self.variable_strategy = "mrv_degree"
            elif strategy == 1:
                # Random ordering
                self.variable_strategy = "random"
                random.shuffle(self.variables)
            elif strategy == 2:
                # Row-first ordering
                self.variable_strategy = "row_first"
                self.variables.sort(key=lambda var: (var[0], var[1]))
            else:
                # Column-first ordering
                self.variable_strategy = "col_first"
                self.variables.sort(key=lambda var: (var[1], var[0]))
            
            # Apply initial constraint propagation
            if not self._initial_constraint_propagation():
                print("No solution exists (detected during initial constraint propagation)")
                continue
            
            # Try to solve with the current restart
            restart_start_time = time.time()
            result = self._backtrack_with_improved_propagation(restart_start_time, timeout_per_restart)
            restart_end_time = time.time()
            
            if result:
                print(f"Solution found in {restart_end_time - start_time:.4f} seconds (restart {restart+1})")
                print(f"Nodes explored: {self.nodes_explored}")
                return True
            else:
                if restart_end_time - restart_start_time >= timeout_per_restart:
                    print(f"Timeout after {timeout_per_restart} seconds on restart {restart+1}")
                elif self.nodes_explored >= self.max_nodes:
                    print(f"Node limit reached ({self.max_nodes}) on restart {restart+1}")
                else:
                    print(f"No solution found on restart {restart+1}")
                print(f"Nodes explored: {self.nodes_explored}")
        
        print(f"No solution found after {max_restarts} restarts")
        return False
    
    def _initial_constraint_propagation(self):
        """
        Apply initial constraint propagation before starting the search.
        Return False if inconsistency is detected.
        """
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
            for i in range(self.size):
                # Check rows
                row_values = [board[i][j] for j in range(self.size)]
                if not self._check_sequence(row_values):
                    if self.debug_level >= 1:
                        print(f"Row {i+1} has more than 2 consecutive identical symbols")
                    return False
                
                # Check columns
                col_values = [board[j][i] for j in range(self.size)]
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
            
            if changed and self.debug_level >= 1:
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
    
    def select_unassigned_variable(self):
        """
        Select an unassigned variable using different strategies based on the current restart
        """
        unassigned = [v for v in self.variables if v not in self.assignment]
        
        if not unassigned:
            return None
        
        if hasattr(self, 'variable_strategy') and self.variable_strategy == "random":
            return random.choice(unassigned)
        elif hasattr(self, 'variable_strategy') and self.variable_strategy in ["row_first", "col_first"]:
            return unassigned[0]  # Already sorted by the strategy
        else:  # Default: MRV + degree
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
        Use a combination of heuristics and randomization.
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
        
        # Count symbols in the row and column
        row_o_count = sum(1 for j in range(self.size) if temp_board[row][j] == 'O')
        row_gt_count = sum(1 for j in range(self.size) if temp_board[row][j] == '>')
        col_o_count = sum(1 for i in range(self.size) if temp_board[i][col] == 'O')
        col_gt_count = sum(1 for i in range(self.size) if temp_board[i][col] == '>')
        
        # Prefer values that balance the row and column
        values = list(self.current_domains[var])
        
        # If we're close to having 3 of one symbol, prefer the other symbol
        if row_o_count >= 2:
            if '>' in values:
                values.remove('>')
                values.insert(0, '>')
        elif row_gt_count >= 2:
            if 'O' in values:
                values.remove('O')
                values.insert(0, 'O')
        
        if col_o_count >= 2:
            if '>' in values:
                values.remove('>')
                values.insert(0, '>')
        elif col_gt_count >= 2:
            if 'O' in values:
                values.remove('O')
                values.insert(0, 'O')
        
        # Occasionally randomize the order to escape local minima
        if random.random() < 0.1:  # 10% chance
            random.shuffle(values)
        
        return values
    
    def _backtrack_with_improved_propagation(self, start_time, timeout):
        """Backtracking algorithm with improved constraint propagation"""
        # Check timeout and node limit
        if time.time() - start_time >= timeout or self.nodes_explored >= self.max_nodes:
            return False
        
        self.nodes_explored += 1
        
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
                domains_updated = True
                for other_var in self.variables:
                    if other_var != var and other_var not in self.assignment:
                        self.current_domains[other_var] = [
                            val for val in self.current_domains[other_var]
                            if self._is_consistent_for_neighbor(other_var, val, self.board)
                        ]
                        if not self.current_domains[other_var]:
                            # Domain wipeout, backtrack
                            domains_updated = False
                            break
                
                if domains_updated:
                    # No domain wipeout, continue with backtracking
                    if self._backtrack_with_improved_propagation(start_time, timeout):
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
        row_values = [board_copy[row][c] for c in range(self.size)]
        if not self._check_sequence(row_values):
            return False
        
        # Check column sequence
        col_values = [board_copy[r][col] for r in range(self.size)]
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
            left_cell = board_copy[row][col-1]
            constraint = self.horizontal_constraints[row][col-1]
            if constraint == 'x' and left_cell == value:
                return False
            if constraint == '=' and left_cell != value:
                return False
        
        if col < self.size - 1 and board_copy[row][col+1] is not None:
            right_cell = board_copy[row][col+1]
            constraint = self.horizontal_constraints[row][col]
            if constraint == 'x' and right_cell == value:
                return False
            if constraint == '=' and right_cell != value:
                return False
        
        # Check vertical constraints
        if row > 0 and board_copy[row-1][col] is not None:
            above_cell = board_copy[row-1][col]
            constraint = self.vertical_constraints[row-1][col]
            if constraint == 'x' and above_cell == value:
                return False
            if constraint == '=' and above_cell != value:
                return False
        
        if row < self.size - 1 and board_copy[row+1][col] is not None:
            below_cell = board_copy[row+1][col]
            constraint = self.vertical_constraints[row][col]
            if constraint == 'x' and below_cell == value:
                return False
            if constraint == '=' and below_cell != value:
                return False
        
        return True
    
    def _print_debug_board(self, board=None):
        """Print the current state of the board"""
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
    print("Complete Fixed Binary Puzzle Solver")
    print("=================================\n")
    
    # Get the constraints from binary_puzzle_example.py
    horizontal_constraints = [
        ['.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.']
    ]
    
    vertical_constraints = [
        ['x', '.', '.', '.', '=', '.'],
        ['.', 'x', '.', '.', '.', 'x'],
        ['x', '.', '.', '.', 'x', '.'],
        ['.', 'x', '.', '.', '.', '='],
        ['x', '.', '.', '.', '=', '.']
    ]
    
    # Initial board from binary_puzzle_example.py
    initial_board = [
        [None, None, 'O', None, None, None],
        [None, None, None, '>', None, None],
        [None, None, '>', None, None, None],
        [None, None, None, 'O', None, None],
        [None, None, 'O', None, None, None],
        [None, None, None, '>', None, None]
    ]
    
    print("Initial board:")
    for row in initial_board:
        print(' '.join(cell if cell is not None else '.' for cell in row))
    
    print("\nSolving with fixed solver and multiple strategies...")
    puzzle = FixedBinaryPuzzleCSP(horizontal_constraints, vertical_constraints, initial_board)
    if puzzle.solve_with_restarts(max_restarts=20, timeout_per_restart=3, total_timeout=60):
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
        
        # Overall verdict
        if (valid_sequence and valid_h_constraints and valid_v_constraints):
            print("\nThe solution is VALID! ✓")
        else:
            print("\nThe solution is INVALID! ✗")
    else:
        print("No solution found")

if __name__ == "__main__":
    main()