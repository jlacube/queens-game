"""
Debug the binary puzzle solver by checking if the user's solution is valid according to our solver's rules
"""

from binary_puzzle_csp import BinaryPuzzleCSP
import numpy as np

def main():
    print("Binary Puzzle Solver Debug")
    print("========================\n")
    
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
    
    print("User's solution:")
    _print_board(user_solution)
    
    # Create a puzzle instance
    puzzle = BinaryPuzzleCSP(horizontal_constraints, vertical_constraints, initial_board)
    
    # Debug: Check if each cell in the user's solution is consistent with our solver's rules
    print("\nChecking each cell in the user's solution...")
    
    # First, fill in the initial values
    for i in range(6):
        for j in range(6):
            if initial_board[i][j] is not None:
                puzzle.assignment[(i, j)] = initial_board[i][j]
    
    # Then check each empty cell
    all_consistent = True
    for i in range(6):
        for j in range(6):
            if initial_board[i][j] is None:
                value = user_solution[i][j]
                is_consistent = puzzle.is_consistent((i, j), value)
                if not is_consistent:
                    all_consistent = False
                    print(f"Cell ({i+1},{j+1}) with value {value} is NOT consistent!")
                    
                    # Debug: Print detailed information about why it's not consistent
                    print(f"  Checking row constraints...")
                    
                    # Create a temporary board with the current assignment and the new value
                    temp_board = [[None for _ in range(6)] for _ in range(6)]
                    for r in range(6):
                        for c in range(6):
                            if puzzle.board[r][c] is not None:
                                temp_board[r][c] = puzzle.board[r][c]
                    
                    for (r, c), v in puzzle.assignment.items():
                        temp_board[r][c] = v
                    
                    temp_board[i][j] = value
                    
                    # Check row sequence
                    row_values = [temp_board[i][c] for c in range(6) if temp_board[i][c] is not None]
                    if not puzzle._check_sequence(row_values):
                        print(f"    Row sequence check failed: {row_values}")
                    
                    # Count symbols in the row
                    row_o_count = sum(1 for c in range(6) if temp_board[i][c] == 'O')
                    row_gt_count = sum(1 for c in range(6) if temp_board[i][c] == '>')
                    if row_o_count > 3 or row_gt_count > 3:
                        print(f"    Row count check failed: {row_o_count} O's, {row_gt_count} >'s")
                    
                    # Check column sequence
                    col_values = [temp_board[r][j] for r in range(6) if temp_board[r][j] is not None]
                    if not puzzle._check_sequence(col_values):
                        print(f"    Column sequence check failed: {col_values}")
                    
                    # Count symbols in the column
                    col_o_count = sum(1 for r in range(6) if temp_board[r][j] == 'O')
                    col_gt_count = sum(1 for r in range(6) if temp_board[r][j] == '>')
                    if col_o_count > 3 or col_gt_count > 3:
                        print(f"    Column count check failed: {col_o_count} O's, {col_gt_count} >'s")
                    
                    # Check horizontal constraints
                    if j > 0:
                        left_cell = temp_board[i][j-1]
                        constraint = horizontal_constraints[i][j-1]
                        if left_cell is not None:
                            if constraint == 'x' and left_cell == value:
                                print(f"    Horizontal constraint 'x' violated with left cell: {left_cell} {constraint} {value}")
                            if constraint == '=' and left_cell != value:
                                print(f"    Horizontal constraint '=' violated with left cell: {left_cell} {constraint} {value}")
                    
                    if j < 5:
                        right_cell = temp_board[i][j+1]
                        constraint = horizontal_constraints[i][j]
                        if right_cell is not None:
                            if constraint == 'x' and right_cell == value:
                                print(f"    Horizontal constraint 'x' violated with right cell: {value} {constraint} {right_cell}")
                            if constraint == '=' and right_cell != value:
                                print(f"    Horizontal constraint '=' violated with right cell: {value} {constraint} {right_cell}")
                    
                    # Check vertical constraints
                    if i > 0:
                        above_cell = temp_board[i-1][j]
                        constraint = vertical_constraints[i-1][j]
                        if above_cell is not None:
                            if constraint == 'x' and above_cell == value:
                                print(f"    Vertical constraint 'x' violated with above cell: {above_cell} {constraint} {value}")
                            if constraint == '=' and above_cell != value:
                                print(f"    Vertical constraint '=' violated with above cell: {above_cell} {constraint} {value}")
                    
                    if i < 5:
                        below_cell = temp_board[i+1][j]
                        constraint = vertical_constraints[i][j]
                        if below_cell is not None:
                            if constraint == 'x' and below_cell == value:
                                print(f"    Vertical constraint 'x' violated with below cell: {value} {constraint} {below_cell}")
                            if constraint == '=' and below_cell != value:
                                print(f"    Vertical constraint '=' violated with below cell: {value} {constraint} {below_cell}")
                else:
                    # Add the value to the assignment and continue
                    puzzle.assignment[(i, j)] = value
    
    if all_consistent:
        print("All cells in the user's solution are consistent with our solver's rules! ✓")
        print("This suggests there might be an issue with our backtracking algorithm.")
    else:
        print("\nSome cells in the user's solution are not consistent with our solver's rules.")
        print("This suggests there might be an issue with our constraint checking.")

def _print_board(board):
    """Print a board in a readable format"""
    for row in board:
        print(' '.join(cell if cell is not None else '.' for cell in row))

if __name__ == "__main__":
    main()