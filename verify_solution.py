"""
Verify the user's solution for the binary puzzle
"""

from binary_puzzle_csp import BinaryPuzzleCSP
import numpy as np

def main():
    print("Binary Puzzle Solution Verification")
    print("================================\n")
    
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
    
    print("\nVerifying if the solution is valid...")
    
    # Check if the solution respects the initial board
    valid_initial = True
    for i in range(6):
        for j in range(6):
            if initial_board[i][j] is not None and initial_board[i][j] != user_solution[i][j]:
                valid_initial = False
                print(f"Error: Solution doesn't match initial board at ({i+1},{j+1})")
                print(f"  Initial: {initial_board[i][j]}, Solution: {user_solution[i][j]}")
    
    if valid_initial:
        print("Solution respects the initial board: ✓")
    else:
        print("Solution doesn't respect the initial board: ✗")
    
    # Check rows
    valid_rows = True
    for i in range(6):
        row = user_solution[i]
        o_count = sum(1 for cell in row if cell == 'O')
        gt_count = sum(1 for cell in row if cell == '>')
        if o_count != 3 or gt_count != 3:
            valid_rows = False
            print(f"Error: Row {i+1} has {o_count} O's and {gt_count} >'s (should be 3 each)")
    
    if valid_rows:
        print("All rows have exactly 3 O's and 3 >'s: ✓")
    else:
        print("Not all rows have exactly 3 O's and 3 >'s: ✗")
    
    # Check columns
    valid_cols = True
    for j in range(6):
        col = [user_solution[i][j] for i in range(6)]
        o_count = sum(1 for cell in col if cell == 'O')
        gt_count = sum(1 for cell in col if cell == '>')
        if o_count != 3 or gt_count != 3:
            valid_cols = False
            print(f"Error: Column {j+1} has {o_count} O's and {gt_count} >'s (should be 3 each)")
    
    if valid_cols:
        print("All columns have exactly 3 O's and 3 >'s: ✓")
    else:
        print("Not all columns have exactly 3 O's and 3 >'s: ✗")
    
    # Check for more than 2 consecutive identical symbols
    valid_sequence = True
    for i in range(6):
        # Check rows
        row = user_solution[i]
        for j in range(2, 6):
            if row[j] == row[j-1] == row[j-2]:
                valid_sequence = False
                print(f"Error: 3 consecutive {row[j]} in row {i+1} at positions {j-2+1}, {j-1+1}, {j+1}")
        
        # Check columns
        col = [user_solution[r][i] for r in range(6)]
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
                left = user_solution[i][j]
                right = user_solution[i][j+1]
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
                top = user_solution[i][j]
                bottom = user_solution[i+1][j]
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
    if (valid_initial and valid_rows and valid_cols and valid_sequence and 
            valid_h_constraints and valid_v_constraints):
        print("\nThe solution is VALID! ✓")
    else:
        print("\nThe solution is INVALID! ✗")
    
    # Now let's try to use our solver to find a solution
    print("\nTrying to use our solver to find a solution...")
    puzzle = BinaryPuzzleCSP(horizontal_constraints, vertical_constraints, initial_board)
    if puzzle.solve():
        print("Our solver found a solution!")
        solution = puzzle.get_solution_board()
        print("\nSolver's solution:")
        _print_board(solution)
    else:
        print("Our solver couldn't find a solution.")
        print("This suggests there might be an issue with our solver implementation.")

def _print_board(board):
    """Print a board in a readable format"""
    for row in board:
        print(' '.join(cell if cell is not None else '.' for cell in row))

if __name__ == "__main__":
    main()