"""
Example usage of the Queens Game Solver
"""

from queens_solver import QueensGameSolver
import numpy as np

def main():
    # Example 1: Solve a 5x5 board with random color regions
    print("Example 1: 5x5 board with random color regions")
    solver = QueensGameSolver(5)
    if solver.solve():
        solver.visualize()
    
    # Example 2: Solve a 6x6 board with custom color regions
    print("\nExample 2: 6x6 board with custom color regions")
    # Create a custom color pattern (6 colors with 6 cells each)
    custom_colors = np.array([
        [0, 1, 2, 3, 4, 5],
        [0, 1, 2, 3, 4, 5],
        [0, 1, 2, 3, 4, 5],
        [0, 1, 2, 3, 4, 5],
        [0, 1, 2, 3, 4, 5],
        [0, 1, 2, 3, 4, 5]
    ])
    solver = QueensGameSolver(6, custom_colors)
    if solver.solve():
        solver.visualize()

if __name__ == "__main__":
    main()