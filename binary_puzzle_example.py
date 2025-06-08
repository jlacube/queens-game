"""
Example usage of the Binary Puzzle Solver
"""

from binary_puzzle_csp import BinaryPuzzleCSP
import numpy as np

def main():
    print("Binary Puzzle Solver Example")
    print("===========================\n")
    
    # Create a 6x6 puzzle with some constraints and initial values
    
    # Horizontal constraints (6x5 grid)
    # 'x' means opposite symbols, '=' means same symbols, '.' means no constraint
    horizontal_constraints = [
        ['.', 'x', '.', '=', '.'],
        ['.', '.', '.', '.', '.'],
        ['.', 'x', '.', 'x', '.'],
        ['.', '=', '.', '=', '.'],
        ['.', '.', '.', '.', '.'],
        ['.', 'x', '.', 'x', '.']
    ]
    
    # Vertical constraints (5x6 grid)
    vertical_constraints = [
        ['.', '.', '.', '.', '.', '.'],
        ['.', '=', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.'],
        ['.', '=', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.']
    ]
    
    # Initial board (6x6 grid)
    # None means empty cell, 'O' or '>' for filled cells
    initial_board = [
        ['O', None, None, None, None, 'O'],
        [None, None, None, None, None, None],
        [None, None, None, None, None, None],
        [None, None, None, None, None, None],
        [None, None, None, None, None, None],
        ['O', None, None, None, None, '>']
    ]
    
    # Create the binary puzzle CSP
    puzzle = BinaryPuzzleCSP(horizontal_constraints, vertical_constraints, initial_board)
    
    print("Initial board:")
    _print_board(initial_board)
    
    print("\nHorizontal constraints:")
    for row in horizontal_constraints:
        print(' '.join(row))
    
    print("\nVertical constraints:")
    for row in vertical_constraints:
        print(' '.join(row))
    
    print("\nSolving...")
    if puzzle.solve():
        print("\nSolution found!")
        
        # Get the solution board
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
        valid = True
        for i in range(6):
            # Check rows
            row = solution[i]
            for j in range(2, 6):
                if row[j] == row[j-1] == row[j-2]:
                    valid = False
                    print(f"Invalid: 3 consecutive {row[j]} in row {i+1}")
            
            # Check columns
            col = [solution[r][i] for r in range(6)]
            for j in range(2, 6):
                if col[j] == col[j-1] == col[j-2]:
                    valid = False
                    print(f"Invalid: 3 consecutive {col[j]} in column {i+1}")
        
        if valid:
            print("No more than 2 consecutive identical symbols: ✓")
        
        # Check constraints
        valid_constraints = True
        
        # Check horizontal constraints
        for i in range(6):
            for j in range(5):
                constraint = horizontal_constraints[i][j]
                if constraint != '.':
                    left = solution[i][j]
                    right = solution[i][j+1]
                    if constraint == 'x' and left == right:
                        valid_constraints = False
                        print(f"Invalid horizontal constraint at ({i+1},{j+1}): {left} {constraint} {right}")
                    elif constraint == '=' and left != right:
                        valid_constraints = False
                        print(f"Invalid horizontal constraint at ({i+1},{j+1}): {left} {constraint} {right}")
        
        # Check vertical constraints
        for i in range(5):
            for j in range(6):
                constraint = vertical_constraints[i][j]
                if constraint != '.':
                    top = solution[i][j]
                    bottom = solution[i+1][j]
                    if constraint == 'x' and top == bottom:
                        valid_constraints = False
                        print(f"Invalid vertical constraint at ({i+1},{j+1}): {top} {constraint} {bottom}")
                    elif constraint == '=' and top != bottom:
                        valid_constraints = False
                        print(f"Invalid vertical constraint at ({i+1},{j+1}): {top} {constraint} {bottom}")
        
        if valid_constraints:
            print("All constraints satisfied: ✓")
        
        # Visualize the solution
        print("\nGenerating visualization...")
        puzzle.visualize()
    else:
        print("No solution exists for this puzzle.")

def _print_board(board):
    """Print a board in a readable format"""
    for row in board:
        print(' '.join(cell if cell is not None else '.' for cell in row))

if __name__ == "__main__":
    main()