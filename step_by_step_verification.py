"""
Step-by-step verification of the user's solution
"""

from binary_puzzle_csp import BinaryPuzzleCSP
import numpy as np

def main():
    print("Step-by-Step Verification of User's Solution")
    print("=========================================\n")
    
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
    
    # Create a puzzle instance
    puzzle = BinaryPuzzleCSP(horizontal_constraints, vertical_constraints, initial_board)
    
    # Step 1: Check if the initial board is respected
    print("\nStep 1: Checking if the initial board is respected...")
    initial_respected = True
    for i in range(6):
        for j in range(6):
            if initial_board[i][j] is not None and initial_board[i][j] != user_solution[i][j]:
                initial_respected = False
                print(f"Error: Initial value at ({i+1},{j+1}) is {initial_board[i][j]}, but solution has {user_solution[i][j]}")
    
    if initial_respected:
        print("Initial board is respected: ✓")
    else:
        print("Initial board is not respected: ✗")
    
    # Step 2: Check row and column counts
    print("\nStep 2: Checking row and column counts...")
    counts_valid = True
    
    # Check rows
    for i in range(6):
        row = user_solution[i]
        o_count = sum(1 for cell in row if cell == 'O')
        gt_count = sum(1 for cell in row if cell == '>')
        if o_count != 3 or gt_count != 3:
            counts_valid = False
            print(f"Error: Row {i+1} has {o_count} O's and {gt_count} >'s (should be 3 each)")
    
    # Check columns
    for j in range(6):
        col = [user_solution[i][j] for i in range(6)]
        o_count = sum(1 for cell in col if cell == 'O')
        gt_count = sum(1 for cell in col if cell == '>')
        if o_count != 3 or gt_count != 3:
            counts_valid = False
            print(f"Error: Column {j+1} has {o_count} O's and {gt_count} >'s (should be 3 each)")
    
    if counts_valid:
        print("All rows and columns have exactly 3 O's and 3 >'s: ✓")
    else:
        print("Not all rows and columns have exactly 3 O's and 3 >'s: ✗")
    
    # Step 3: Check for consecutive identical symbols
    print("\nStep 3: Checking for consecutive identical symbols...")
    consecutive_valid = True
    
    # Check rows
    for i in range(6):
        row = user_solution[i]
        for j in range(2, 6):
            if row[j] == row[j-1] == row[j-2]:
                consecutive_valid = False
                print(f"Error: 3 consecutive {row[j]} in row {i+1} at positions {j-2+1}, {j-1+1}, {j+1}")
    
    # Check columns
    for j in range(6):
        col = [user_solution[i][j] for i in range(6)]
        for i in range(2, 6):
            if col[i] == col[i-1] == col[i-2]:
                consecutive_valid = False
                print(f"Error: 3 consecutive {col[i]} in column {j+1} at positions {i-2+1}, {i-1+1}, {i+1}")
    
    if consecutive_valid:
        print("No more than 2 consecutive identical symbols: ✓")
    else:
        print("There are more than 2 consecutive identical symbols: ✗")
    
    # Step 4: Check horizontal constraints
    print("\nStep 4: Checking horizontal constraints...")
    h_constraints_valid = True
    
    for i in range(6):
        for j in range(5):
            constraint = horizontal_constraints[i][j]
            if constraint != '.':
                left = user_solution[i][j]
                right = user_solution[i][j+1]
                if constraint == 'x' and left == right:
                    h_constraints_valid = False
                    print(f"Error: Horizontal constraint 'x' violated at ({i+1},{j+1}): {left} {constraint} {right}")
                elif constraint == '=' and left != right:
                    h_constraints_valid = False
                    print(f"Error: Horizontal constraint '=' violated at ({i+1},{j+1}): {left} {constraint} {right}")
    
    if h_constraints_valid:
        print("All horizontal constraints are satisfied: ✓")
    else:
        print("Not all horizontal constraints are satisfied: ✗")
    
    # Step 5: Check vertical constraints
    print("\nStep 5: Checking vertical constraints...")
    v_constraints_valid = True
    
    for i in range(5):
        for j in range(6):
            constraint = vertical_constraints[i][j]
            if constraint != '.':
                top = user_solution[i][j]
                bottom = user_solution[i+1][j]
                if constraint == 'x' and top == bottom:
                    v_constraints_valid = False
                    print(f"Error: Vertical constraint 'x' violated at ({i+1},{j+1}): {top} {constraint} {bottom}")
                elif constraint == '=' and top != bottom:
                    v_constraints_valid = False
                    print(f"Error: Vertical constraint '=' violated at ({i+1},{j+1}): {top} {constraint} {bottom}")
    
    if v_constraints_valid:
        print("All vertical constraints are satisfied: ✓")
    else:
        print("Not all vertical constraints are satisfied: ✗")
    
    # Step 6: Try to build the solution step by step
    print("\nStep 6: Building the solution step by step...")
    
    # Start with the initial board
    board = [[None for _ in range(6)] for _ in range(6)]
    for i in range(6):
        for j in range(6):
            if initial_board[i][j] is not None:
                board[i][j] = initial_board[i][j]
    
    # Print the initial state
    print("\nInitial state:")
    _print_board(board)
    
    # Try to fill in the board step by step using the user's solution
    steps = []
    for i in range(6):
        for j in range(6):
            if board[i][j] is None:
                # Try to place the user's solution value
                value = user_solution[i][j]
                
                # Check if this placement is valid
                valid = True
                
                # Check row for consecutive identical symbols
                row = [board[i][k] if board[i][k] is not None else value if k == j else None for k in range(6)]
                for k in range(2, 6):
                    if row[k] is not None and row[k-1] is not None and row[k-2] is not None:
                        if row[k] == row[k-1] == row[k-2]:
                            valid = False
                            print(f"Cannot place {value} at ({i+1},{j+1}): Would create 3 consecutive {value} in row {i+1}")
                
                # Check column for consecutive identical symbols
                col = [board[k][j] if board[k][j] is not None else value if k == i else None for k in range(6)]
                for k in range(2, 6):
                    if col[k] is not None and col[k-1] is not None and col[k-2] is not None:
                        if col[k] == col[k-1] == col[k-2]:
                            valid = False
                            print(f"Cannot place {value} at ({i+1},{j+1}): Would create 3 consecutive {value} in column {j+1}")
                
                # Check horizontal constraints
                if j > 0 and board[i][j-1] is not None:
                    constraint = horizontal_constraints[i][j-1]
                    if constraint == 'x' and board[i][j-1] == value:
                        valid = False
                        print(f"Cannot place {value} at ({i+1},{j+1}): Would violate horizontal constraint 'x' with ({i+1},{j})")
                    elif constraint == '=' and board[i][j-1] != value:
                        valid = False
                        print(f"Cannot place {value} at ({i+1},{j+1}): Would violate horizontal constraint '=' with ({i+1},{j})")
                
                if j < 5 and board[i][j+1] is not None:
                    constraint = horizontal_constraints[i][j]
                    if constraint == 'x' and board[i][j+1] == value:
                        valid = False
                        print(f"Cannot place {value} at ({i+1},{j+1}): Would violate horizontal constraint 'x' with ({i+1},{j+2})")
                    elif constraint == '=' and board[i][j+1] != value:
                        valid = False
                        print(f"Cannot place {value} at ({i+1},{j+1}): Would violate horizontal constraint '=' with ({i+1},{j+2})")
                
                # Check vertical constraints
                if i > 0 and board[i-1][j] is not None:
                    constraint = vertical_constraints[i-1][j]
                    if constraint == 'x' and board[i-1][j] == value:
                        valid = False
                        print(f"Cannot place {value} at ({i+1},{j+1}): Would violate vertical constraint 'x' with ({i},{j+1})")
                    elif constraint == '=' and board[i-1][j] != value:
                        valid = False
                        print(f"Cannot place {value} at ({i+1},{j+1}): Would violate vertical constraint '=' with ({i},{j+1})")
                
                if i < 5 and board[i+1][j] is not None:
                    constraint = vertical_constraints[i][j]
                    if constraint == 'x' and board[i+1][j] == value:
                        valid = False
                        print(f"Cannot place {value} at ({i+1},{j+1}): Would violate vertical constraint 'x' with ({i+2},{j+1})")
                    elif constraint == '=' and board[i+1][j] != value:
                        valid = False
                        print(f"Cannot place {value} at ({i+1},{j+1}): Would violate vertical constraint '=' with ({i+2},{j+1})")
                
                if valid:
                    board[i][j] = value
                    steps.append((i, j, value))
                    print(f"Placed {value} at ({i+1},{j+1})")
                else:
                    print(f"Cannot place {value} at ({i+1},{j+1}) according to our constraint checking")
    
    # Print the final state
    print("\nFinal state after step-by-step building:")
    _print_board(board)
    
    # Check if the final state matches the user's solution
    matches_user = True
    for i in range(6):
        for j in range(6):
            if board[i][j] != user_solution[i][j]:
                matches_user = False
                print(f"Final state differs from user's solution at ({i+1},{j+1}): {board[i][j]} vs {user_solution[i][j]}")
    
    if matches_user:
        print("\nThe step-by-step built solution matches the user's solution! ✓")
    else:
        print("\nThe step-by-step built solution differs from the user's solution. ✗")
        print("This suggests there might be an issue with our constraint checking.")

def _print_board(board):
    """Print a board in a readable format"""
    for row in board:
        print(' '.join(cell if cell is not None else '.' for cell in row))

if __name__ == "__main__":
    main()