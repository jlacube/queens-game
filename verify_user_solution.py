"""
Verify the user's solution by directly setting it as the assignment and checking if it's valid
"""

from binary_puzzle_csp import BinaryPuzzleCSP
import numpy as np

def main():
    print("Verify User's Solution")
    print("=====================\n")
    
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
    
    # Set the assignment to the user's solution
    for i in range(6):
        for j in range(6):
            if initial_board[i][j] is None:  # Only set variables that are not in the initial board
                puzzle.assignment[(i, j)] = user_solution[i][j]
    
    # Check if the assignment is valid
    print("\nChecking if the assignment is valid...")
    
    # Check if all variables are assigned
    if len(puzzle.assignment) == len(puzzle.variables):
        print("All variables are assigned: ✓")
    else:
        print(f"Not all variables are assigned: ✗ ({len(puzzle.assignment)} of {len(puzzle.variables)})")
    
    # Check if the assignment is consistent
    all_consistent = True
    # Create a copy of the assignment dictionary to avoid modifying it during iteration
    assignment_items = list(puzzle.assignment.items())
    for var, value in assignment_items:
        # Temporarily remove this assignment to check if it's consistent
        temp_value = puzzle.assignment[var]
        del puzzle.assignment[var]
        
        if not puzzle.is_consistent(var, temp_value):
            all_consistent = False
            print(f"Assignment {var} = {temp_value} is not consistent!")
        
        # Restore the assignment
        puzzle.assignment[var] = temp_value
    
    if all_consistent:
        print("All assignments are consistent: ✓")
    else:
        print("Not all assignments are consistent: ✗")
    
    # Check if the solution satisfies all constraints
    print("\nVerifying solution constraints...")
    
    # Check rows
    for i in range(6):
        row = user_solution[i]
        o_count = sum(1 for cell in row if cell == 'O')
        gt_count = sum(1 for cell in row if cell == '>')
        print(f"Row {i+1}: {o_count} O's, {gt_count} >'s - ", end="")
        print("✓" if o_count == 3 and gt_count == 3 else "✗")
    
    # Check columns
    for j in range(6):
        col = [user_solution[i][j] for i in range(6)]
        o_count = sum(1 for cell in col if cell == 'O')
        gt_count = sum(1 for cell in col if cell == '>')
        print(f"Column {j+1}: {o_count} O's, {gt_count} >'s - ", end="")
        print("✓" if o_count == 3 and gt_count == 3 else "✗")
    
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
    if (all_consistent and valid_sequence and valid_h_constraints and valid_v_constraints):
        print("\nThe user's solution is VALID according to our constraint checking! ✓")
        print("This suggests there might be an issue with our backtracking algorithm.")
    else:
        print("\nThe user's solution is INVALID according to our constraint checking! ✗")
        print("This suggests there might be a discrepancy between our understanding of the constraints.")

def _print_board(board):
    """Print a board in a readable format"""
    for row in board:
        print(' '.join(cell if cell is not None else '.' for cell in row))

if __name__ == "__main__":
    main()