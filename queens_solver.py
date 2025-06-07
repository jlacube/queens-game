"""
Queens Game Solver with Color Constraints

Rules:
- Exactly one queen in each row, column, and color region
- Queens cannot touch each other, not even diagonally (minimum distance of 2)
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import random
import time

class QueensGameSolver:
    def __init__(self, n, color_regions=None):
        """
        Initialize the solver for an n x n board
        
        Args:
            n: Size of the board (n x n)
            color_regions: Optional 2D array specifying color regions (0 to n-1)
                          If None, random color regions will be generated
        """
        self.n = n
        self.board = np.zeros((n, n), dtype=int)  # 0 = empty, 1 = queen
        
        # Generate or use provided color regions
        if color_regions is None:
            self.color_regions = self._generate_color_regions()
        else:
            self.color_regions = color_regions
            
        # Track queens placed in each color
        self.queens_in_color = [0] * n
        
    def _generate_color_regions(self):
        """Generate random color regions with exactly n cells of each color"""
        # Start with a list of n² cells, with n cells of each color
        cells = []
        for color in range(self.n):
            cells.extend([color] * self.n)
            
        # Shuffle the cells
        random.shuffle(cells)
        
        # Reshape into an n x n grid
        return np.array(cells).reshape(self.n, self.n)
    
    def is_valid_position(self, row, col):
        """Check if placing a queen at (row, col) is valid"""
        # Check if there's already a queen in this row or column
        for i in range(self.n):
            if self.board[row][i] == 1 or self.board[i][col] == 1:
                return False
        
        # Check if there's already a queen in this color region
        color = self.color_regions[row][col]
        if self.queens_in_color[color] > 0:
            return False
        
        # Check if this position touches another queen (including diagonally)
        # We need to check all positions at distance 1
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue  # Skip the current position
                
                r, c = row + dr, col + dc
                if 0 <= r < self.n and 0 <= c < self.n and self.board[r][c] == 1:
                    return False
        
        return True
    
    def solve(self):
        """Solve the queens game using backtracking"""
        start_time = time.time()
        result = self._backtrack(0)
        end_time = time.time()
        
        if result:
            print(f"Solution found in {end_time - start_time:.4f} seconds")
            return True
        else:
            print("No solution exists")
            return False
    
    def _backtrack(self, row):
        """Backtracking algorithm to place queens"""
        if row == self.n:
            return True  # All queens are placed successfully
        
        for col in range(self.n):
            if self.is_valid_position(row, col):
                # Place the queen
                self.board[row][col] = 1
                color = self.color_regions[row][col]
                self.queens_in_color[color] += 1
                
                # Recursively place the rest of the queens
                if self._backtrack(row + 1):
                    return True
                
                # If placing a queen here doesn't lead to a solution, backtrack
                self.board[row][col] = 0
                self.queens_in_color[color] -= 1
        
        return False  # No valid position in this row
    
    def visualize(self):
        """Visualize the board with queens and color regions"""
        fig, ax = plt.subplots(figsize=(10, 10))
        
        # Create a colormap for the color regions
        # Generate n distinct colors manually
        colors = []
        for i in range(self.n):
            # Generate colors using HSV color space for better distinction
            hue = i / self.n
            # Convert HSV to RGB (simplified approach)
            h = hue * 6
            c = 1
            x = c * (1 - abs(h % 2 - 1))
            
            if h < 1:
                r, g, b = c, x, 0
            elif h < 2:
                r, g, b = x, c, 0
            elif h < 3:
                r, g, b = 0, c, x
            elif h < 4:
                r, g, b = 0, x, c
            elif h < 5:
                r, g, b = x, 0, c
            else:
                r, g, b = c, 0, x
                
            # Add alpha channel
            colors.append([r, g, b, 1.0])
            
        cmap = ListedColormap(colors)
        
        # Plot the color regions
        im = ax.imshow(self.color_regions, cmap=cmap, alpha=0.5)
        
        # Add grid lines
        ax.set_xticks(np.arange(-0.5, self.n, 1), minor=True)
        ax.set_yticks(np.arange(-0.5, self.n, 1), minor=True)
        ax.grid(which='minor', color='black', linestyle='-', linewidth=2)
        
        # Add queens
        for i in range(self.n):
            for j in range(self.n):
                if self.board[i][j] == 1:
                    ax.text(j, i, '♕', fontsize=24, ha='center', va='center')
        
        # Remove ticks
        ax.set_xticks([])
        ax.set_yticks([])
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax, ticks=np.arange(self.n))
        cbar.set_label('Color Regions')
        
        plt.title(f"Queens Game Solution (n={self.n})")
        plt.tight_layout()
        plt.savefig(f"queens_solution_n{self.n}.png")
        plt.show()

# Example usage
if __name__ == "__main__":
    # Solve for different board sizes
    for n in range(4, 9):
        print(f"\nSolving for n = {n}")
        solver = QueensGameSolver(n)
        if solver.solve():
            solver.visualize()