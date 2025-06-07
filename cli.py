"""
Command-line interface for the Queens Game Solver
"""

import argparse
import numpy as np
from queens_solver import QueensGameSolver

def main():
    parser = argparse.ArgumentParser(description='Solve the Queens Game with color constraints')
    parser.add_argument('-n', '--size', type=int, default=5, help='Size of the board (n x n)')
    parser.add_argument('-c', '--color-pattern', choices=['random', 'columns', 'rows', 'blocks'], 
                        default='random', help='Color pattern to use')
    parser.add_argument('-o', '--output', type=str, default=None, 
                        help='Output file for the visualization (default: queens_solution_n{size}.png)')
    parser.add_argument('--no-display', action='store_true', 
                        help='Do not display the visualization (only save to file)')
    
    args = parser.parse_args()
    
    # Create color regions based on the selected pattern
    color_regions = None
    if args.color_pattern != 'random':
        color_regions = np.zeros((args.size, args.size), dtype=int)
        
        if args.color_pattern == 'columns':
            # Each column is a different color
            for col in range(args.size):
                color_regions[:, col] = col
        
        elif args.color_pattern == 'rows':
            # Each row is a different color
            for row in range(args.size):
                color_regions[row, :] = row
        
        elif args.color_pattern == 'blocks':
            # Create block pattern (if size is a perfect square)
            block_size = int(np.sqrt(args.size))
            if block_size * block_size != args.size:
                print(f"Warning: Size {args.size} is not a perfect square. Using random pattern instead.")
                color_regions = None
            else:
                for i in range(block_size):
                    for j in range(block_size):
                        color_regions[i*block_size:(i+1)*block_size, j*block_size:(j+1)*block_size] = i * block_size + j
    
    # Create and run the solver
    solver = QueensGameSolver(args.size, color_regions)
    if solver.solve():
        # Customize visualization
        import matplotlib.pyplot as plt
        
        # Override the default visualization method to handle CLI options
        def custom_visualize():
            fig, ax = plt.subplots(figsize=(10, 10))
            
            # Create a colormap for the color regions
            # Generate n distinct colors manually
            colors = []
            for i in range(solver.n):
                # Generate colors using HSV color space for better distinction
                hue = i / solver.n
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
                
            from matplotlib.colors import ListedColormap
            cmap = ListedColormap(colors)
            
            # Plot the color regions
            im = ax.imshow(solver.color_regions, cmap=cmap, alpha=0.5)
            
            # Add grid lines
            ax.set_xticks(np.arange(-0.5, solver.n, 1), minor=True)
            ax.set_yticks(np.arange(-0.5, solver.n, 1), minor=True)
            ax.grid(which='minor', color='black', linestyle='-', linewidth=2)
            
            # Add queens
            for i in range(solver.n):
                for j in range(solver.n):
                    if solver.board[i][j] == 1:
                        ax.text(j, i, '♕', fontsize=24, ha='center', va='center')
            
            # Remove ticks
            ax.set_xticks([])
            ax.set_yticks([])
            
            # Add colorbar
            cbar = plt.colorbar(im, ax=ax, ticks=np.arange(solver.n))
            cbar.set_label('Color Regions')
            
            plt.title(f"Queens Game Solution (n={solver.n}, pattern={args.color_pattern})")
            plt.tight_layout()
            
            # Save to file
            output_file = args.output if args.output else f"queens_solution_n{solver.n}_{args.color_pattern}.png"
            plt.savefig(output_file)
            print(f"Solution saved to {output_file}")
            
            # Display if requested
            if not args.no_display:
                plt.show()
        
        # Call our custom visualization
        custom_visualize()
    else:
        print("No solution exists for the given parameters.")

if __name__ == "__main__":
    main()