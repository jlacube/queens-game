"""
Examples of using the CSP solver framework for different problem types
"""

import numpy as np
from csp_solver import MapColoringCSP, SudokuCSP
from queens_csp import QueensGameCSP

def queens_game_example():
    """Example of solving the Queens Game with color constraints"""
    print("\n=== Queens Game Example ===\n")
    
    # Create a 5x5 board with diagonal color regions
    n = 5
    color_regions = np.zeros((n, n), dtype=int)
    
    # Fill the color regions diagonally
    for i in range(n):
        for j in range(n):
            color_regions[i, j] = (i + j) % n
    
    print("Board size:", n, "x", n)
    print("\nColor regions:")
    print(color_regions)
    
    # Create and solve the Queens Game CSP
    queens_csp = QueensGameCSP(n, color_regions)
    
    if queens_csp.solve():
        print("\nSolution found!")
        
        # Get the board representation
        board = queens_csp.get_board()
        print("\nBoard with queens (1 = queen, 0 = empty):")
        print(board)
        
        # Print the solution in a more readable format
        print("\nSolution visualization:")
        for i in range(n):
            row = ""
            for j in range(n):
                if board[i, j] == 1:
                    row += "Q "
                else:
                    row += ". "
            print(row)
        
        # Verify the solution meets all constraints
        print("\nVerifying solution...")
        
        # Check one queen per row
        row_valid = all(sum(board[i]) == 1 for i in range(n))
        print("One queen per row:", "✓" if row_valid else "✗")
        
        # Check one queen per column
        col_valid = all(sum(board[:, i]) == 1 for i in range(n))
        print("One queen per column:", "✓" if col_valid else "✗")
        
        # Check one queen per color
        queens_in_color = [0] * n
        for i in range(n):
            for j in range(n):
                if board[i, j] == 1:
                    color = color_regions[i, j]
                    queens_in_color[color] += 1
        
        color_valid = all(count == 1 for count in queens_in_color)
        print("One queen per color:", "✓" if color_valid else "✗")
        
        # Check queens don't touch
        touching = False
        for i in range(n):
            for j in range(n):
                if board[i, j] == 1:
                    # Check all adjacent cells (including diagonals)
                    for di in [-1, 0, 1]:
                        for dj in [-1, 0, 1]:
                            if di == 0 and dj == 0:
                                continue
                            ni, nj = i + di, j + dj
                            if 0 <= ni < n and 0 <= nj < n and board[ni, nj] == 1:
                                touching = True
        
        print("Queens don't touch:", "✓" if not touching else "✗")
        
        # Display the solution
        print("\nGenerating visualization...")
        queens_csp.visualize()
    else:
        print("No solution exists for this board configuration.")


def map_coloring_example():
    """Example of solving a Map Coloring problem"""
    print("\n=== Map Coloring Example ===\n")
    
    # Define the regions (states/countries)
    regions = ['WA', 'NT', 'SA', 'Q', 'NSW', 'V', 'T']
    
    # Define the neighbors for each region
    neighbors = {
        'WA': ['NT', 'SA'],
        'NT': ['WA', 'SA', 'Q'],
        'SA': ['WA', 'NT', 'Q', 'NSW', 'V'],
        'Q': ['NT', 'SA', 'NSW'],
        'NSW': ['Q', 'SA', 'V'],
        'V': ['SA', 'NSW'],
        'T': []  # Tasmania has no neighbors
    }
    
    # Define the available colors
    colors = ['red', 'green', 'blue']
    
    print("Regions:", regions)
    print("Colors:", colors)
    print("\nNeighbors:")
    for region, neighbors_list in neighbors.items():
        print(f"{region}: {', '.join(neighbors_list)}")
    
    # Create and solve the Map Coloring CSP
    map_csp = MapColoringCSP(regions, neighbors, colors)
    
    if map_csp.solve():
        print("\nSolution found!")
        map_csp.visualize()
    else:
        print("No solution exists for this map coloring problem.")


def sudoku_example():
    """Example of solving a Sudoku puzzle"""
    print("\n=== Sudoku Example ===\n")
    
    # Define a Sudoku puzzle (0 represents empty cells)
    grid = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
    
    print("Sudoku Puzzle:")
    for i in range(9):
        if i > 0 and i % 3 == 0:
            print("-" * 21)
        
        row = ""
        for j in range(9):
            if j > 0 and j % 3 == 0:
                row += "| "
            if grid[i][j] == 0:
                row += ". "
            else:
                row += f"{grid[i][j]} "
        
        print(row)
    
    # Create and solve the Sudoku CSP
    sudoku_csp = SudokuCSP(grid)
    
    if sudoku_csp.solve():
        print("\nSolution found!")
        sudoku_csp.visualize()
    else:
        print("No solution exists for this Sudoku puzzle.")


if __name__ == "__main__":
    # Run all examples
    queens_game_example()
    map_coloring_example()
    sudoku_example()