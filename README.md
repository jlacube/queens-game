# Constraint Satisfaction Problem (CSP) Solver

This project implements a generic framework for solving Constraint Satisfaction Problems (CSPs), with a focus on the Queens Game with color constraints.

## Queens Game Rules

- Your goal is to have exactly one queen in each row, column, and color region.
- Two queens cannot touch each other, not even diagonally (minimum distance of 2).

## Project Overview

The project consists of two main parts:
1. A specialized Queens Game solver
2. A generalized CSP framework that can solve various constraint satisfaction problems

## Installation

1. Clone this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Project Structure

### Specialized Queens Game Solver

- **queens_solver.py**: Original implementation of the Queens Game solver
- **example.py**: Example usage with random and custom color regions
- **cli.py**: Command-line interface for easy experimentation
- **demo.py**: Demonstration script with a specific example
- **test_solver.py**: Test suite for the Queens Game solver

### Generalized CSP Framework

- **csp_solver.py**: Generic CSP solver framework with base classes and implementations for:
  - Map Coloring problems
  - Sudoku puzzles
- **queens_csp.py**: Implementation of the Queens Game using the CSP framework
- **csp_examples.py**: Examples of using the CSP framework for different problem types

## Usage

### Queens Game Solver

Run the example script to see the specialized Queens Game solver in action:

```bash
python example.py
```

This will solve two example boards:
1. A 5x5 board with randomly generated color regions
2. A 6x6 board with custom color regions (columns as color regions)

### Command Line Interface

The project includes a command-line interface for easy experimentation with the Queens Game:

```bash
python cli.py --help
```

Examples:

```bash
# Solve a 5x5 board with random color regions
python cli.py -n 5 -c random

# Solve a 6x6 board with columns as color regions
python cli.py -n 6 -c columns

# Solve a 4x4 board with rows as color regions and save to a specific file
python cli.py -n 4 -c rows -o my_solution.png

# Solve a 9x9 board with block pattern (3x3 blocks) without displaying
python cli.py -n 9 -c blocks --no-display
```

### Demo Script

A demonstration script with a specific Queens Game example:

```bash
python demo.py
```

This script creates a 5x5 board with diagonal color regions, solves it, and verifies that the solution meets all constraints.

### CSP Examples

Run the CSP examples script to see the generalized solver in action:

```bash
python csp_examples.py
```

This will solve three different types of constraint satisfaction problems:
1. Queens Game with color constraints
2. Map Coloring problem (Australia map)
3. Sudoku puzzle

### Running Tests

To verify that the Queens Game solver works correctly:

```bash
python -m unittest test_solver.py
```

### Custom Usage

You can create your own instances of the solver:

```python
from queens_solver import QueensGameSolver
import numpy as np

# Create a solver for a 5x5 board with random color regions
solver = QueensGameSolver(5)
if solver.solve():
    solver.visualize()

# Create a solver with custom color regions
custom_colors = np.array([
    [0, 1, 2, 3],
    [0, 1, 2, 3],
    [0, 1, 2, 3],
    [0, 1, 2, 3]
])
solver = QueensGameSolver(4, custom_colors)
if solver.solve():
    solver.visualize()
```

## How It Works

### Queens Game Solver

The specialized Queens Game solver uses a backtracking algorithm to find a valid placement of queens on the board. It enforces the following constraints:

1. Exactly one queen in each row
2. Exactly one queen in each column
3. Exactly one queen in each color region
4. Queens cannot touch each other (minimum distance of 2)

The solution is visualized using matplotlib, showing the color regions and queen placements.

### CSP Framework

The generalized CSP framework provides a flexible approach to solving constraint satisfaction problems:

1. **Variables**: The objects to which values must be assigned
2. **Domains**: The possible values each variable can take
3. **Constraints**: Rules that restrict the values that variables can take simultaneously

The framework uses a backtracking algorithm with these key components:
- Variable selection heuristics (e.g., Minimum Remaining Values)
- Value ordering heuristics
- Constraint checking
- Backtracking search

## Extending the Framework

You can easily extend the CSP framework to solve other types of constraint satisfaction problems:

1. Create a new class that inherits from the `CSP` base class
2. Implement the required methods:
   - `get_variables()`: Define the variables in your problem
   - `get_domains()`: Define the possible values for each variable
   - `get_constraints()`: Define the constraints between variables
   - `visualize()`: Implement a visualization method for your problem

Example:

```python
from csp_solver import CSP

class MyCustomCSP(CSP):
    def __init__(self, problem_data):
        self.problem_data = problem_data
        super().__init__()
    
    def get_variables(self):
        # Return a list of variables
        return [...]
    
    def get_domains(self):
        # Return a dictionary mapping variables to their domains
        return {var: [...] for var in self.variables}
    
    def get_constraints(self):
        # Return a list of constraints
        constraints = []
        # Add constraints...
        return constraints
    
    def visualize(self):
        # Implement visualization for your problem
        pass
```

## Output

The solvers will generate visualizations of the solutions and save them as PNG files. They will also display the solutions in matplotlib windows if run in an interactive environment.