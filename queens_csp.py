"""
Queens Game Solver using the CSP framework

This module implements the Queens Game with color constraints as a Constraint Satisfaction Problem.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import random
from typing import Dict, List, Tuple, Any

from csp_solver import CSP


class QueensGameCSP(CSP):
    """
    Queens Game CSP: Place queens on a board such that:
    - Exactly one queen in each row, column, and color region
    - Queens cannot touch each other, not even diagonally
    """
    
    def __init__(self, n, color_regions=None):
        """
        Initialize the Queens Game CSP.
        
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
        
        super().__init__()
    
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
    
    def get_variables(self):
        """Variables are the rows of the board (since we need one queen per row)"""
        return list(range(self.n))
    
    def get_domains(self):
        """Domain for each row is the set of columns (since we need one queen per column)"""
        return {row: list(range(self.n)) for row in range(self.n)}
    
    def get_constraints(self):
        """Define the constraints for the Queens Game"""
        constraints = []
        
        # 1. One queen per column constraint
        def column_constraint(assignment):
            # Check if all columns are different
            return len(set(assignment.values())) == len(assignment)
        
        constraints.append((self.variables, column_constraint))
        
        # 2. One queen per color region constraint
        def color_constraint(assignment):
            # Check if all queens are in different color regions
            colors_used = set()
            for row, col in assignment.items():
                color = self.color_regions[row][col]
                if color in colors_used:
                    return False
                colors_used.add(color)
            return True
        
        constraints.append((self.variables, color_constraint))
        
        # 3. Queens cannot touch constraint
        def no_touch_constraint(assignment):
            # Check if any queens are touching
            positions = [(row, col) for row, col in assignment.items()]
            for i, (row1, col1) in enumerate(positions):
                for row2, col2 in positions[i+1:]:
                    # Calculate distance between queens
                    row_dist = abs(row1 - row2)
                    col_dist = abs(col1 - col2)
                    
                    # Queens touch if they are adjacent (including diagonally)
                    if row_dist <= 1 and col_dist <= 1:
                        return False
            return True
        
        constraints.append((self.variables, no_touch_constraint))
        
        return constraints
    
    def is_consistent(self, var, value) -> bool:
        """
        Override the default is_consistent method for efficiency.
        
        This method checks if placing a queen at position (var, value) is consistent
        with the current assignment, without having to check all constraints.
        """
        # Check if the column is already used
        if value in self.assignment.values():
            return False
        
        # Check if the color is already used
        color = self.color_regions[var][value]
        for row, col in self.assignment.items():
            if self.color_regions[row][col] == color:
                return False
        
        # Check if the queen touches any other queen
        for row, col in self.assignment.items():
            row_dist = abs(var - row)
            col_dist = abs(value - col)
            if row_dist <= 1 and col_dist <= 1:
                return False
        
        return True
    
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
        for row, col in self.assignment.items():
            ax.text(col, row, '♕', fontsize=24, ha='center', va='center')
        
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
    
    def get_board(self):
        """Convert the assignment to a board representation"""
        board = np.zeros((self.n, self.n), dtype=int)
        for row, col in self.assignment.items():
            board[row][col] = 1
        return board