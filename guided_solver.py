"""
Guided solver that uses the user's solution as a hint
"""

from binary_puzzle_csp import BinaryPuzzleCSP
import time

class GuidedBinaryPuzzleCSP(BinaryPuzzleCSP):
    """
    A version of the Binary Puzzle CSP that uses the user's solution as a hint
    """
    
    def __init__(self, horizontal_constraints=None, vertical_constraints=None, initial_board=None, hint_solution=None):
        """
        Initialize the Guided Binary Puzzle CSP.
        
        Args:
            horizontal_constraints: 6x5 grid of constraints between horizontal cells ('x', '=', or '.')
            vertical_constraints: 5x6 grid of constraints between vertical cells ('x', '=', or '.')
            initial_board: 6x6 grid with initial values (None for empty cells, 'O' or '>' for filled cells)
            hint_solution: The solution to use as a hint
        """
        super().__init__(horizontal_constraints, vertical_constraints, initial_board)
        self.hint_solution = hint_solution
    
    def order_domain_values(self, var):
        """
        Order domain values to try the hint value first.
        """
        row, col = var
        if self.hint_solution and self.hint_solution[row][col] in self.domains[var]:
            # Try the hint value first
            hint_value = self.hint_solution[row][col]
            other_values = [v for v in self.domains[var] if v != hint_value]
            return [hint_value] + other_values
        else:
            # Fall back to the default ordering
            return super().order_domain_values(var)
    
    def solve_with_increasing_timeout(self, start_timeout=1, max_timeout=60, factor=2):
        """
        Solve the CSP with increasing timeouts.
        
        Args:
            start_timeout: Initial timeout in seconds
            max_timeout: Maximum timeout in seconds
            factor: Factor to increase the timeout by each time
        """
        timeout = start_timeout
        while timeout <= max_timeout:
            print(f"Trying with timeout {timeout} seconds...")
            if self.solve(timeout):
                return True
            timeout *= factor
        
        print(f"Failed to find a solution within {max_timeout} seconds")
        return False

def main():
    print("Guided Binary Puzzle Solver")
    print("==========================\n")
    
    # User's solution
    user_solution = [
        ['O', '>', 'O', '>', '>', 'O'],
        ['>', 'O', 'O', '>', 'O', '>'],
        ['>', 'O', '>', 'O', '>', 'O'],
        ['O', '>', '>', 'O', 'O', '>'],
        ['>', '>', 'O', '>', 'O', 'O'],
        ['O', 'O', '>', 'O', '>', '>']
    ]
    
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
    
    print("\nUser's solution:")
    _print_board(user_solution)
    
    # Try solving without hints first
    print("\nSolving without hints...")
    start_time = time.time()
    puzzle = BinaryPuzzleCSP(horizontal_constraints, vertical_constraints, initial_board)
    if puzzle.solve(timeout=5):
        end_time = time.time()
        print(f"Solution found in {end_time - start_time:.4f} seconds")
        solution = puzzle.get_solution_board()
        print("\nSolution:")
        _print_board(solution)
    else:
        print("No solution found without hints")
    
    # Try solving with hints
    print("\nSolving with hints...")
    start_time = time.time()
    guided_puzzle = GuidedBinaryPuzzleCSP(horizontal_constraints, vertical_constraints, initial_board, user_solution)
    if guided_puzzle.solve(timeout=5):
        end_time = time.time()
        print(f"Solution found in {end_time - start_time:.4f} seconds")
        solution = guided_puzzle.get_solution_board()
        print("\nSolution:")
        _print_board(solution)
        
        # Check if the solution matches the user's solution
        matches_user = True
        for i in range(6):
            for j in range(6):
                if solution[i][j] != user_solution[i][j]:
                    matches_user = False
                    print(f"Solution differs from user's solution at ({i+1},{j+1})")
        
        if matches_user:
            print("\nThe solution matches the user's solution! ✓")
        else:
            print("\nThe solution differs from the user's solution, but is still valid.")
    else:
        print("No solution found even with hints")
        
        # Try with increasing timeouts
        print("\nTrying with increasing timeouts...")
        guided_puzzle = GuidedBinaryPuzzleCSP(horizontal_constraints, vertical_constraints, initial_board, user_solution)
        if guided_puzzle.solve_with_increasing_timeout():
            solution = guided_puzzle.get_solution_board()
            print("\nSolution:")
            _print_board(solution)
            
            # Check if the solution matches the user's solution
            matches_user = True
            for i in range(6):
                for j in range(6):
                    if solution[i][j] != user_solution[i][j]:
                        matches_user = False
                        print(f"Solution differs from user's solution at ({i+1},{j+1})")
            
            if matches_user:
                print("\nThe solution matches the user's solution! ✓")
            else:
                print("\nThe solution differs from the user's solution, but is still valid.")
        else:
            print("Failed to find a solution even with increasing timeouts")

def _print_board(board):
    """Print a board in a readable format"""
    for row in board:
        print(' '.join(cell if cell is not None else '.' for cell in row))

if __name__ == "__main__":
    main()