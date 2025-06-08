"""
Generic Constraint Satisfaction Problem (CSP) Solver

This module provides a framework for defining and solving constraint satisfaction problems.
"""

import time
from abc import ABC, abstractmethod
from typing import Dict, List, Set, Tuple, Any, Callable, Optional


class CSP(ABC):
    """
    Abstract base class for Constraint Satisfaction Problems.
    
    To use this class, create a subclass and implement the required methods.
    """
    
    def __init__(self):
        """Initialize the CSP"""
        self.variables = self.get_variables()
        self.domains = self.get_domains()
        self.constraints = self.get_constraints()
        self.assignment = {}  # Current assignment of values to variables
    
    @abstractmethod
    def get_variables(self) -> List[Any]:
        """
        Return a list of all variables in the problem.
        
        Each variable can be any hashable type.
        """
        pass
    
    @abstractmethod
    def get_domains(self) -> Dict[Any, List[Any]]:
        """
        Return a dictionary mapping each variable to its domain.
        
        The domain is a list of possible values for the variable.
        """
        pass
    
    @abstractmethod
    def get_constraints(self) -> List[Tuple[List[Any], Callable]]:
        """
        Return a list of constraints.
        
        Each constraint is a tuple (scope, predicate) where:
        - scope is a list of variables involved in the constraint
        - predicate is a function that takes an assignment (dict mapping variables to values)
          and returns True if the constraint is satisfied, False otherwise
        """
        pass
    
    def is_complete(self) -> bool:
        """Check if the current assignment is complete"""
        return len(self.assignment) == len(self.variables)
    
    def is_consistent(self, var, value) -> bool:
        """Check if assigning value to var is consistent with current assignment"""
        # Create a temporary assignment with the new variable-value pair
        assignment = self.assignment.copy()
        assignment[var] = value
        
        # Check all constraints involving var
        for scope, predicate in self.constraints:
            if var in scope:
                # Only check constraints where all variables in scope are assigned
                if all(v in assignment for v in scope):
                    # Extract the values for the variables in scope
                    values = {v: assignment[v] for v in scope}
                    if not predicate(values):
                        return False
        
        return True
    
    def select_unassigned_variable(self) -> Any:
        """
        Select an unassigned variable.
        
        Default implementation uses Minimum Remaining Values (MRV) heuristic.
        """
        unassigned = [v for v in self.variables if v not in self.assignment]
        
        # Use MRV heuristic: choose variable with fewest legal values
        return min(unassigned, key=lambda var: sum(
            1 for value in self.domains[var] if self.is_consistent(var, value)
        ))
    
    def order_domain_values(self, var) -> List[Any]:
        """
        Order the domain values for a variable.
        
        Default implementation returns the domain values in their original order.
        """
        return self.domains[var]
    
    def solve(self) -> bool:
        """Solve the CSP using backtracking"""
        start_time = time.time()
        result = self._backtrack()
        end_time = time.time()
        
        if result:
            print(f"Solution found in {end_time - start_time:.4f} seconds")
            return True
        else:
            print("No solution exists")
            return False
    
    def _backtrack(self) -> bool:
        """Backtracking algorithm to find a solution"""
        if self.is_complete():
            return True
        
        var = self.select_unassigned_variable()
        
        for value in self.order_domain_values(var):
            if self.is_consistent(var, value):
                # Assign value to var
                self.assignment[var] = value
                
                # Recursively try to complete the assignment
                if self._backtrack():
                    return True
                
                # If we get here, this assignment didn't work
                del self.assignment[var]
        
        return False
    
    @abstractmethod
    def visualize(self):
        """Visualize the solution"""
        pass


class MapColoringCSP(CSP):
    """
    Map Coloring CSP: Assign colors to regions such that no adjacent regions have the same color.
    """
    
    def __init__(self, regions, neighbors, colors):
        """
        Initialize the Map Coloring CSP.
        
        Args:
            regions: List of regions to color
            neighbors: Dict mapping each region to its adjacent regions
            colors: List of available colors
        """
        self.regions = regions
        self.neighbors = neighbors
        self.colors = colors
        super().__init__()
    
    def get_variables(self):
        return self.regions
    
    def get_domains(self):
        return {region: self.colors.copy() for region in self.regions}
    
    def get_constraints(self):
        constraints = []
        
        # Add a constraint for each pair of neighboring regions
        for region, neighbors in self.neighbors.items():
            for neighbor in neighbors:
                # Only add the constraint once for each pair
                if region < neighbor:
                    # Create a constraint: neighboring regions must have different colors
                    scope = [region, neighbor]
                    
                    def predicate(assignment, r=region, n=neighbor):
                        return assignment[r] != assignment[n]
                    
                    constraints.append((scope, predicate))
        
        return constraints
    
    def visualize(self):
        """Visualize the map coloring solution"""
        print("\nMap Coloring Solution:")
        for region in sorted(self.regions):
            print(f"{region}: {self.assignment.get(region, 'Not assigned')}")


class SudokuCSP(CSP):
    """
    Sudoku CSP: Fill a 9x9 grid with digits 1-9 such that each row, column, and 3x3 box
    contains each digit exactly once.
    """
    
    def __init__(self, grid):
        """
        Initialize the Sudoku CSP.
        
        Args:
            grid: 9x9 grid with initial values (0 for empty cells)
        """
        self.grid = [row[:] for row in grid]  # Make a deep copy
        self.size = len(grid)
        self.box_size = int(self.size ** 0.5)  # Size of each 3x3 box
        super().__init__()
    
    def get_variables(self):
        # Variables are the empty cells in the grid
        variables = []
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == 0:
                    variables.append((i, j))
        return variables
    
    def get_domains(self):
        domains = {}
        for var in self.variables:
            i, j = var
            if self.grid[i][j] == 0:
                domains[var] = list(range(1, self.size + 1))
            else:
                domains[var] = [self.grid[i][j]]
        return domains
    
    def get_constraints(self):
        # For Sudoku, we'll implement the constraints directly in is_consistent
        # This is more efficient than checking all constraints for each assignment
        return []
    
    def is_consistent(self, var, value) -> bool:
        """
        Check if assigning value to var is consistent with current assignment.
        For Sudoku, we need to check row, column, and box constraints.
        """
        i, j = var
        
        # Check if this value is already used in the same row
        for col in range(self.size):
            if col != j:
                # Check if this cell is in the current assignment or in the initial grid
                if (i, col) in self.assignment and self.assignment[(i, col)] == value:
                    return False
                elif (i, col) not in self.variables and self.grid[i][col] == value:
                    return False
        
        # Check if this value is already used in the same column
        for row in range(self.size):
            if row != i:
                # Check if this cell is in the current assignment or in the initial grid
                if (row, j) in self.assignment and self.assignment[(row, j)] == value:
                    return False
                elif (row, j) not in self.variables and self.grid[row][j] == value:
                    return False
        
        # Check if this value is already used in the same 3x3 box
        box_i, box_j = i // self.box_size, j // self.box_size
        for row in range(box_i * self.box_size, (box_i + 1) * self.box_size):
            for col in range(box_j * self.box_size, (box_j + 1) * self.box_size):
                if row != i or col != j:
                    # Check if this cell is in the current assignment or in the initial grid
                    if (row, col) in self.assignment and self.assignment[(row, col)] == value:
                        return False
                    elif (row, col) not in self.variables and self.grid[row][col] == value:
                        return False
        
        return True
    
    def visualize(self):
        """Visualize the Sudoku solution"""
        print("\nSudoku Solution:")
        
        # Create a grid with the solution
        solution = [row[:] for row in self.grid]
        for (i, j), value in self.assignment.items():
            solution[i][j] = value
        
        # Print the grid
        for i in range(self.size):
            if i > 0 and i % self.box_size == 0:
                print("-" * (self.size * 2 + self.box_size - 1))
            
            row = ""
            for j in range(self.size):
                if j > 0 and j % self.box_size == 0:
                    row += "| "
                row += f"{solution[i][j]} "
            
            print(row)