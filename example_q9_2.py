"""
Example usage of the Queens Game Solver
"""

from queens_solver import QueensGameSolver
import numpy as np

def main():
    # Example 1: Solve a 9x9 board with custom color regions
    print("\nExample 1: 9x9 board with custom color regions")
    # Create a custom color pattern (9 colors with 9 cells each)
    custom_colors = np.array([
        [0, 0, 1, 1, 1, 1, 1, 1, 2],
        [3, 0, 4, 4, 4, 4, 1, 1, 2],
        [0, 0, 0, 4, 4, 4, 4, 2, 2],
        [5, 5, 5, 6, 6, 4, 4, 2, 2],
        [5, 7, 5, 5, 6, 4, 4, 4, 2],
        [5, 7, 5, 6, 6, 6, 4, 2, 2],
        [5, 7, 7, 7, 7, 7, 8, 8, 2],
        [5, 7, 7, 7, 7, 7, 7, 8, 2],
        [7, 7, 7, 7, 7, 7, 8, 8, 8],
    ])
    solver = QueensGameSolver(9, custom_colors)
    if solver.solve():
        solver.visualize()

if __name__ == "__main__":
    main()