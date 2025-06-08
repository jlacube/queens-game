"""
Enhanced Binary Puzzle Solver with advanced constraint propagation techniques
"""

from binary_puzzle_csp import BinaryPuzzleCSP
import time
import copy

class EnhancedBinaryPuzzleCSP(BinaryPuzzleCSP):
    """
    Enhanced Binary Puzzle CSP with advanced constraint propagation techniques
    """
    
    def solve(self, timeout=30) -> bool:
        """
        Solve the CSP using backtracking with constraint propagation and a timeout.
        
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
        result = self._backtrack_with_constraint_propagation(start_time, timeout)
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
            
            # Check for constraint violations
            for i in range(self.size):
                # Check rows
                row_values = [board[i][j] for j in range(self.size) if board[i][j] is not None]
                if not self._check_sequence(row_values):
                    return False
                
                # Check columns
                col_values = [board[j][i] for j in range(self.size) if board[j][i] is not None]
                if not self._check_sequence(col_values):
                    return False
            
            # Check horizontal constraints
            for i in range(self.size):
                for j in range(self.size-1):
                    constraint = self.horizontal_constraints[i][j]
                    if constraint != '.' and board[i][j] is not None and board[i][j+1] is not None:
                        if constraint == 'x' and board[i][j] == board[i][j+1]:
                            return False
                        if constraint == '=' and board[i][j] != board[i][j+1]:
                            return False
            
            # Check vertical constraints
            for i in range(self.size-1):
                for j in range(self.size):
                    constraint = self.vertical_constraints[i][j]
                    if constraint != '.' and board[i][j] is not None and board[i+1][j] is not None:
                        if constraint == 'x' and board[i][j] == board[i+1][j]:
                            return False
                        if constraint == '=' and board[i][j] != board[i+1][j]:
                            return False
        
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
    
    def _backtrack_with_constraint_propagation(self, start_time, timeout) -> bool:
        """Backtracking algorithm with constraint propagation to find a solution"""
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
                
                # Save current domains and board state
                saved_domains = {v: list(self.current_domains[v]) for v in self.variables if v != var}
                saved_board = copy.deepcopy(self.board)
                
                # Apply constraint propagation
                self.board[var[0]][var[1]] = value
                if self._constraint_propagation():
                    # Recursively try to complete the assignment
                    if self._backtrack_with_constraint_propagation(start_time, timeout):
                        return True
                
                # If we get here, this assignment didn't work
                del self.assignment[var]
                
                # Restore domains and board
                for v in saved_domains:
                    self.current_domains[v] = saved_domains[v]
                self.board = saved_board
        
        return False
    
    def _constraint_propagation(self) -> bool:
        """
        Apply constraint propagation after each assignment.
        Return False if inconsistency is detected.
        """
        # Create a working board with the current assignment
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
            
            # Check for constraint violations
            for i in range(self.size):
                # Check rows
                row_values = [board[i][j] for j in range(self.size) if board[i][j] is not None]
                if not self._check_sequence(row_values):
                    return False
                
                # Check columns
                col_values = [board[j][i] for j in range(self.size) if board[j][i] is not None]
                if not self._check_sequence(col_values):
                    return False
        
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

def main():
    print("Enhanced Binary Puzzle Solver")
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
    
    print("\nSolving with enhanced constraint propagation...")
    puzzle = EnhancedBinaryPuzzleCSP(horizontal_constraints, vertical_constraints, initial_board)
    if puzzle.solve(timeout=30):
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