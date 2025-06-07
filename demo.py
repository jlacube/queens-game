"""
Demo script for the Queens Game Solver with a specific example
"""

import numpy as np
from queens_solver import QueensGameSolver

def main():
    """Run a demonstration of the Queens Game Solver with a specific example"""
    print("Queens Game Solver Demo")
    print("======================\n")
    
    # Create a 5x5 board with a specific color pattern
    # In this pattern, we'll create diagonal color regions
    n = 5
    color_regions = np.zeros((n, n), dtype=int)
    
    # Fill the color regions diagonally
    for i in range(n):
        for j in range(n):
            color_regions[i, j] = (i + j) % n
    
    print("Board size:", n, "x", n)
    print("\nColor regions:")
    print(color_regions)
    
    # Create and run the solver
    solver = QueensGameSolver(n, color_regions)
    
    print("\nSolving...")
    if solver.solve():
        print("\nSolution found!")
        print("\nBoard with queens (1 = queen, 0 = empty):")
        print(solver.board)
        
        # Print the solution in a more readable format
        print("\nSolution visualization:")
        for i in range(n):
            row = ""
            for j in range(n):
                if solver.board[i, j] == 1:
                    row += "Q "
                else:
                    row += ". "
            print(row)
        
        # Verify the solution meets all constraints
        print("\nVerifying solution...")
        
        # Check one queen per row
        row_valid = all(sum(solver.board[i]) == 1 for i in range(n))
        print("One queen per row:", "✓" if row_valid else "✗")
        
        # Check one queen per column
        col_valid = all(sum(solver.board[:, i]) == 1 for i in range(n))
        print("One queen per column:", "✓" if col_valid else "✗")
        
        # Check one queen per color
        queens_in_color = [0] * n
        for i in range(n):
            for j in range(n):
                if solver.board[i, j] == 1:
                    color = color_regions[i, j]
                    queens_in_color[color] += 1
        
        color_valid = all(count == 1 for count in queens_in_color)
        print("One queen per color:", "✓" if color_valid else "✗")
        
        # Check queens don't touch
        touching = False
        for i in range(n):
            for j in range(n):
                if solver.board[i, j] == 1:
                    # Check all adjacent cells (including diagonals)
                    for di in [-1, 0, 1]:
                        for dj in [-1, 0, 1]:
                            if di == 0 and dj == 0:
                                continue
                            ni, nj = i + di, j + dj
                            if 0 <= ni < n and 0 <= nj < n and solver.board[ni, nj] == 1:
                                touching = True
        
        print("Queens don't touch:", "✓" if not touching else "✗")
        
        # Display the solution
        print("\nGenerating visualization...")
        solver.visualize()
    else:
        print("No solution exists for this board configuration.")

if __name__ == "__main__":
    main()