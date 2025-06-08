"""
Detailed verification of the user's solution to understand why our solvers can't find it
"""

from binary_puzzle_csp import BinaryPuzzleCSP
import numpy as np

def main():
    print("Detailed Verification of User's Solution")
    print("=======================================\n")
    
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
    
    # Verify the solution step by step
    print("\nVerifying solution step by step...\n")
    
    # Check if the solution matches the initial board
    print("1. Checking if the solution matches the initial board:")
    matches_initial = True
    for i in range(6):
        for j in range(6):
            if initial_board[i][j] is not None and user_solution[i][j] != initial_board[i][j]:
                matches_initial = False
                print(f"   ✗ Mismatch at ({i+1},{j+1}): Initial board has {initial_board[i][j]}, solution has {user_solution[i][j]}")
    
    if matches_initial:
        print("   ✓ Solution matches all initial values")
    
    # Check rows
    print("\n2. Checking rows:")
    for i in range(6):
        row = user_solution[i]
        o_count = sum(1 for cell in row if cell == 'O')
        gt_count = sum(1 for cell in row if cell == '>')
        print(f"   Row {i+1}: {o_count} O's, {gt_count} >'s - ", end="")
        print("✓" if o_count == 3 and gt_count == 3 else "✗")
    
    # Check columns
    print("\n3. Checking columns:")
    for j in range(6):
        col = [user_solution[i][j] for i in range(6)]
        o_count = sum(1 for cell in col if cell == 'O')
        gt_count = sum(1 for cell in col if cell == '>')
        print(f"   Column {j+1}: {o_count} O's, {gt_count} >'s - ", end="")
        print("✓" if o_count == 3 and gt_count == 3 else "✗")
    
    # Check for more than 2 consecutive identical symbols
    print("\n4. Checking for more than 2 consecutive identical symbols:")
    valid_sequence = True
    for i in range(6):
        # Check rows
        row = user_solution[i]
        for j in range(2, 6):
            if row[j] == row[j-1] == row[j-2]:
                valid_sequence = False
                print(f"   ✗ Row {i+1} has 3 consecutive {row[j]} at positions {j-2+1}, {j-1+1}, {j+1}")
        
        # Check columns
        col = [user_solution[r][i] for r in range(6)]
        for j in range(2, 6):
            if col[j] == col[j-1] == col[j-2]:
                valid_sequence = False
                print(f"   ✗ Column {i+1} has 3 consecutive {col[j]} at positions {j-2+1}, {j-1+1}, {j+1}")
    
    if valid_sequence:
        print("   ✓ No more than 2 consecutive identical symbols")
    
    # Check horizontal constraints
    print("\n5. Checking horizontal constraints:")
    valid_h_constraints = True
    for i in range(6):
        for j in range(5):
            constraint = horizontal_constraints[i][j]
            if constraint != '.':
                left = user_solution[i][j]
                right = user_solution[i][j+1]
                if constraint == 'x' and left == right:
                    valid_h_constraints = False
                    print(f"   ✗ Horizontal constraint 'x' violated at ({i+1},{j+1}): {left} {constraint} {right}")
                elif constraint == '=' and left != right:
                    valid_h_constraints = False
                    print(f"   ✗ Horizontal constraint '=' violated at ({i+1},{j+1}): {left} {constraint} {right}")
    
    if valid_h_constraints:
        print("   ✓ All horizontal constraints are satisfied")
    
    # Check vertical constraints
    print("\n6. Checking vertical constraints:")
    valid_v_constraints = True
    for i in range(5):
        for j in range(6):
            constraint = vertical_constraints[i][j]
            if constraint != '.':
                top = user_solution[i][j]
                bottom = user_solution[i+1][j]
                if constraint == 'x' and top == bottom:
                    valid_v_constraints = False
                    print(f"   ✗ Vertical constraint 'x' violated at ({i+1},{j+1}): {top} {constraint} {bottom}")
                elif constraint == '=' and top != bottom:
                    valid_v_constraints = False
                    print(f"   ✗ Vertical constraint '=' violated at ({i+1},{j+1}): {top} {constraint} {bottom}")
    
    if valid_v_constraints:
        print("   ✓ All vertical constraints are satisfied")
    
    # Overall verdict
    print("\nOverall verdict:")
    if (matches_initial and valid_sequence and valid_h_constraints and valid_v_constraints):
        print("✓ The user's solution is VALID according to all constraints!")
        print("This suggests there might be an issue with our solver algorithm.")
    else:
        print("✗ The user's solution is INVALID according to our constraints!")
        print("This explains why our solvers can't find this solution.")
        
        # List all violations
        print("\nConstraint violations:")
        if not matches_initial:
            print("- Solution doesn't match the initial board")
        
        for i in range(6):
            row = user_solution[i]
            o_count = sum(1 for cell in row if cell == 'O')
            gt_count = sum(1 for cell in row if cell == '>')
            if o_count != 3 or gt_count != 3:
                print(f"- Row {i+1} has {o_count} O's and {gt_count} >'s (should be 3 each)")
        
        for j in range(6):
            col = [user_solution[i][j] for i in range(6)]
            o_count = sum(1 for cell in col if cell == 'O')
            gt_count = sum(1 for cell in col if cell == '>')
            if o_count != 3 or gt_count != 3:
                print(f"- Column {j+1} has {o_count} O's and {gt_count} >'s (should be 3 each)")
        
        if not valid_sequence:
            print("- There are more than 2 consecutive identical symbols")
        
        if not valid_h_constraints:
            print("- Horizontal constraints are violated")
        
        if not valid_v_constraints:
            print("- Vertical constraints are violated")
    
    # Check if the solution is valid according to the CSP framework
    print("\nVerifying with the CSP framework:")
    puzzle = BinaryPuzzleCSP(horizontal_constraints, vertical_constraints, initial_board)
    
    # Set the assignment to the user's solution
    for i in range(6):
        for j in range(6):
            if initial_board[i][j] is None:  # Only set variables that are not in the initial board
                puzzle.assignment[(i, j)] = user_solution[i][j]
    
    # Check if the assignment is valid
    all_consistent = True
    # Create a copy of the assignment dictionary to avoid modifying it during iteration
    assignment_items = list(puzzle.assignment.items())
    for var, value in assignment_items:
        # Temporarily remove this assignment to check if it's consistent
        temp_value = puzzle.assignment[var]
        del puzzle.assignment[var]
        
        if not puzzle.is_consistent(var, temp_value):
            all_consistent = False
            print(f"✗ Assignment {var} = {temp_value} is not consistent according to the CSP framework!")
            
            # Check why it's not consistent
            row, col = var
            
            # Create a temporary board with the current assignment and the new value
            temp_board = [[None for _ in range(puzzle.size)] for _ in range(puzzle.size)]
            for i in range(puzzle.size):
                for j in range(puzzle.size):
                    if puzzle.board[i][j] is not None:
                        temp_board[i][j] = puzzle.board[i][j]
            
            for (r, c), v in puzzle.assignment.items():
                temp_board[r][c] = v
            temp_board[row][col] = temp_value
            
            # Check row constraints
            row_values = [temp_board[row][c] for c in range(puzzle.size) if temp_board[row][c] is not None]
            if not puzzle._check_sequence(row_values):
                print(f"  - Row {row+1} would have more than 2 consecutive identical symbols")
            
            # Count symbols in the row
            row_o_count = sum(1 for c in range(puzzle.size) if temp_board[row][c] == 'O')
            row_gt_count = sum(1 for c in range(puzzle.size) if temp_board[row][c] == '>')
            
            # Check if we've exceeded the maximum allowed symbols per row
            if row_o_count > 3:
                print(f"  - Row {row+1} would have more than 3 O's ({row_o_count})")
            if row_gt_count > 3:
                print(f"  - Row {row+1} would have more than 3 >'s ({row_gt_count})")
            
            # Check column constraints
            col_values = [temp_board[r][col] for r in range(puzzle.size) if temp_board[r][col] is not None]
            if not puzzle._check_sequence(col_values):
                print(f"  - Column {col+1} would have more than 2 consecutive identical symbols")
            
            # Count symbols in the column
            col_o_count = sum(1 for r in range(puzzle.size) if temp_board[r][col] == 'O')
            col_gt_count = sum(1 for r in range(puzzle.size) if temp_board[r][col] == '>')
            
            # Check if we've exceeded the maximum allowed symbols per column
            if col_o_count > 3:
                print(f"  - Column {col+1} would have more than 3 O's ({col_o_count})")
            if col_gt_count > 3:
                print(f"  - Column {col+1} would have more than 3 >'s ({col_gt_count})")
            
            # Check horizontal constraints between cells
            if col > 0:
                left_cell = temp_board[row][col-1]
                constraint = horizontal_constraints[row][col-1]
                if left_cell is not None and constraint != '.':
                    if constraint == 'x' and left_cell == temp_value:
                        print(f"  - Would violate horizontal constraint 'x' with ({row+1},{col})")
                    if constraint == '=' and left_cell != temp_value:
                        print(f"  - Would violate horizontal constraint '=' with ({row+1},{col})")
            
            if col < puzzle.size - 1:
                right_cell = temp_board[row][col+1]
                constraint = horizontal_constraints[row][col]
                if right_cell is not None and constraint != '.':
                    if constraint == 'x' and right_cell == temp_value:
                        print(f"  - Would violate horizontal constraint 'x' with ({row+1},{col+2})")
                    if constraint == '=' and right_cell != temp_value:
                        print(f"  - Would violate horizontal constraint '=' with ({row+1},{col+2})")
            
            # Check vertical constraints between cells
            if row > 0:
                above_cell = temp_board[row-1][col]
                constraint = vertical_constraints[row-1][col]
                if above_cell is not None and constraint != '.':
                    if constraint == 'x' and above_cell == temp_value:
                        print(f"  - Would violate vertical constraint 'x' with ({row},{col+1})")
                    if constraint == '=' and above_cell != temp_value:
                        print(f"  - Would violate vertical constraint '=' with ({row},{col+1})")
            
            if row < puzzle.size - 1:
                below_cell = temp_board[row+1][col]
                constraint = vertical_constraints[row][col]
                if below_cell is not None and constraint != '.':
                    if constraint == 'x' and below_cell == temp_value:
                        print(f"  - Would violate vertical constraint 'x' with ({row+2},{col+1})")
                    if constraint == '=' and below_cell != temp_value:
                        print(f"  - Would violate vertical constraint '=' with ({row+2},{col+1})")
        
        # Restore the assignment
        puzzle.assignment[var] = temp_value
    
    if all_consistent:
        print("✓ All assignments are consistent according to the CSP framework!")
    
    # Check if the solution satisfies all constraints
    print("\nFinal verdict:")
    if all_consistent and matches_initial and valid_sequence and valid_h_constraints and valid_v_constraints:
        print("✓ The user's solution is VALID according to all checks!")
        print("This suggests there might be an issue with our solver algorithm.")
    else:
        print("✗ The user's solution is INVALID according to at least one check!")
        print("This explains why our solvers can't find this solution.")

def _print_board(board):
    """Print a board in a readable format"""
    for row in board:
        print(' '.join(cell if cell is not None else '.' for cell in row))

if __name__ == "__main__":
    main()