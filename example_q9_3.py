"""
Example usage of the Queens Game Solver using the CSP framework
"""

from queens_csp import QueensGameCSP
import numpy as np

def main():
    # Example 1: Solve a 9x9 board with custom color regions
    print("\nExample 1: 9x9 board with custom color regions")
    # Create a custom color pattern (9 colors with 9 cells each)
    custom_colors = np.array([
        [0, 0, 0, 0, 0, 0, 0, 1],
        [0, 2, 2, 3, 3, 3, 0, 1],
        [0, 2, 4, 4, 4, 3, 0, 1],
        [0, 2, 5, 6, 4, 3, 0, 1],
        [7, 2, 5, 6, 6, 3, 0, 1],
        [7, 2, 5, 5, 5, 5, 0, 1],
        [7, 2, 2, 2, 0, 0, 0, 1],
        [7, 7, 1, 1, 1, 1, 1, 1],
    ])
    
    # Create and solve the Queens Game CSP
    solver = QueensGameCSP(8, custom_colors)
    
    print("Solving using the CSP framework...")
    if solver.solve():
        print("Solution found!")
        
        # Get the board representation
        board = solver.get_board()
        
        # Print the solution in a readable format
        print("\nSolution visualization:")
        for i in range(8):
            row = ""
            for j in range(8):
                if board[i, j] == 1:
                    row += "Q "
                else:
                    row += ". "
            print(row)
        
        # Visualize the solution
        solver.visualize()
    else:
        print("No solution exists for this board configuration.")

if __name__ == "__main__":
    main()