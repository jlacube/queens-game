# Queens Game Solver with Color Constraints

This project implements a solver for a modified version of the Queens Game with additional color constraints.

## Rules

- Your goal is to have exactly one queen in each row, column, and color region.
- Two queens cannot touch each other, not even diagonally (minimum distance of 2).

## Installation

1. Clone this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run the example script to see the solver in action:

```bash
python example.py
```

This will solve two example boards:
1. A 5x5 board with randomly generated color regions
2. A 6x6 board with custom color regions (columns as color regions)

### Command Line Interface

The project includes a command-line interface for easy experimentation:

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

A demonstration script with a specific example is included:

```bash
python demo.py
```

This script creates a 5x5 board with diagonal color regions, solves it, and verifies that the solution meets all constraints.

### Running Tests

To verify that the solver works correctly:

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

The solver uses a backtracking algorithm to find a valid placement of queens on the board. It enforces the following constraints:

1. Exactly one queen in each row
2. Exactly one queen in each column
3. Exactly one queen in each color region
4. Queens cannot touch each other (minimum distance of 2)

The solution is visualized using matplotlib, showing the color regions and queen placements.

## Output

The solver will generate a visualization of the solution and save it as a PNG file. It will also display the solution in a matplotlib window if run in an interactive environment.