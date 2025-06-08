"""
Binary Puzzle Solver with a known solution
"""

from binary_puzzle_csp import BinaryPuzzleCSP
import numpy as np

def main():
    print("Binary Puzzle Solver - Known Solution Example")
    print("=========================================\n")
    
    # Define a puzzle with a known solution
    
    # The solution we want to find
    solution = [
        ['O', '>', 'O', '>', 'O', '>'],
        ['>', 'O', '>', 'O', '>', 'O'],
        ['O', '>', 'O', '>', 'O', '>'],
        ['>', 'O', '>', 'O', '>', 'O'],
        ['O', '>', 'O', '>', 'O', '>'],
        ['>', 'O', '>', 'O', '>', 'O']
    ]
    
    # Create an initial board with some of the values from the solution
    initial_board = [
        ['O', None, None, None, None, '>'],
        [None, 'O', None, None, None, None],
        [None, None, 'O', None, None, None],
        [None, None, None, 'O', None, None],
        [None, None, None, None, 'O', None],
        [None, None, None, None, None, 'O']
    ]
    
    # No constraints needed for this example
    horizontal_constraints = [
        ['.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.']
    ]
    
    vertical_constraints = [
        ['.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.']
    ]
    
    # Create the binary puzzle CSP
    puzzle = BinaryPuzzleCSP(horizontal_constraints, vertical_constraints, initial_board)
    
    print("Initial board:")
    _print_board(initial_board)
    
    print("\nExpected solution:")
    _print_board(solution)
    
    print("\nSolving...")
    if puzzle.solve():
        print("\nSolution found!")
        
        # Get the solution board
        found_solution = puzzle.get_solution_board()
        
        print("\nFound solution:")
        _print_board(found_solution)
        
        # Check if the found solution matches the expected solution
        matches_expected = True
        for i in range(6):
            for j in range(6):
                if found_solution[i][j] != solution[i][j]:
                    matches_expected = False
                    print(f"Mismatch at ({i+1},{j+1}): Expected {solution[i][j]}, found {found_solution[i][j]}")
        
        if matches_expected:
            print("\nThe found solution matches the expected solution! ✓")
        else:
            print("\nThe found solution does not match the expected solution. ✗")
            print("However, let's verify if it's still a valid solution:")
        
        # Verify the solution
        print("\nVerifying solution...")
        
        # Check rows
        for i in range(6):
            row = found_solution[i]
            o_count = sum(1 for cell in row if cell == 'O')
            gt_count = sum(1 for cell in row if cell == '>')
            print(f"Row {i+1}: {o_count} O's, {gt_count} >'s - ", end="")
            print("✓" if o_count == 3 and gt_count == 3 else "✗")
        
        # Check columns
        for j in range(6):
            col = [found_solution[i][j] for i in range(6)]
            o_count = sum(1 for cell in col if cell == 'O')
            gt_count = sum(1 for cell in col if cell == '>')
            print(f"Column {j+1}: {o_count} O's, {gt_count} >'s - ", end="")
            print("✓" if o_count == 3 and gt_count == 3 else "✗")
        
        # Check for more than 2 consecutive identical symbols
        valid = True
        for i in range(6):
            # Check rows
            row = found_solution[i]
            for j in range(2, 6):
                if row[j] == row[j-1] == row[j-2]:
                    valid = False
                    print(f"Invalid: 3 consecutive {row[j]} in row {i+1}")
            
            # Check columns
            col = [found_solution[r][i] for r in range(6)]
            for j in range(2, 6):
                if col[j] == col[j-1] == col[j-2]:
                    valid = False
                    print(f"Invalid: 3 consecutive {col[j]} in column {i+1}")
        
        if valid:
            print("No more than 2 consecutive identical symbols: ✓")
        
        # Visualize the solution
        print("\nGenerating visualization...")
        puzzle.visualize()
    else:
        print("No solution exists for this puzzle.")
        print("This is unexpected since we provided a known solution!")

def _print_board(board):
    """Print a board in a readable format"""
    for row in board:
        print(' '.join(cell if cell is not None else '.' for cell in row))

if __name__ == "__main__":
    main()