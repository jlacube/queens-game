"""
Fixed Binary Puzzle Solver that correctly handles the consecutive symbols check
"""

from binary_puzzle_csp import BinaryPuzzleCSP
import time
import copy
from typing import List, Dict, Tuple, Optional, Any, Union

class FixedBinaryPuzzleCSP(BinaryPuzzleCSP):
    """
    Fixed Binary Puzzle CSP with corrected _check_sequence method
    """
    
    def _check_sequence(self, values):
        """
        FIXED: Check if a sequence of values has no more than 2 consecutive identical symbols.
        This version properly handles None values by only considering consecutive positions.
        
        Args:
            values: List of values ('O', '>', or None)
        """
        # Don't filter out None values, but track consecutive positions
        consecutive_count = 1
        last_symbol = None
        
        for value in values:
            if value is None:
                # None values break consecutive sequences
                consecutive_count = 1
                last_symbol = None
                continue
                
            if last_symbol is None:
                # First non-None value in a sequence
                last_symbol = value
                consecutive_count = 1
            elif value == last_symbol:
                # Same symbol as previous
                consecutive_count += 1
                if consecutive_count > 2:
                    return False
            else:
                # Different symbol
                last_symbol = value
                consecutive_count = 1
                
        return True
    
    def debug_check_sequence(self, values):
        """
        Debug version of _check_sequence that explains the checking process
        """
        print(f"Checking sequence: {values}")
        
        consecutive_count = 1
        last_symbol = None
        
        for i, value in enumerate(values):
            if value is None:
                print(f"  Position {i+1}: None - Breaking consecutive sequence")
                consecutive_count = 1
                last_symbol = None
                continue
                
            if last_symbol is None:
                print(f"  Position {i+1}: {value} - First non-None value")
                last_symbol = value
                consecutive_count = 1
            elif value == last_symbol:
                consecutive_count += 1
                print(f"  Position {i+1}: {value} - Same as previous, count = {consecutive_count}")
                if consecutive_count > 2:
                    print(f"  Found more than 2 consecutive {value} symbols!")
                    return False
            else:
                print(f"  Position {i+1}: {value} - Different from previous, resetting count")
                last_symbol = value
                consecutive_count = 1
                
        print("  Sequence is valid (no more than 2 consecutive identical symbols)")
        return True

def main():
    print("Fixed Binary Puzzle Solver Test")
    print("=============================\n")
    
    # Test the fixed _check_sequence method
    solver = FixedBinaryPuzzleCSP()
    
    # Test cases
    test_cases = [
        # Valid sequences
        ['O', '>', 'O', '>', 'O', '>'],  # Alternating
        ['O', 'O', '>', '>', 'O', 'O'],  # Two consecutive, then different
        ['O', None, 'O', None, 'O'],     # Non-consecutive with None
        ['O', None, None, 'O', None, 'O'],  # Non-consecutive with multiple None
        ['>', '>', 'O', 'O', '>', '>'],  # Two consecutive at start and end
        
        # Invalid sequences
        ['O', 'O', 'O', '>', '>', '>'],  # Three consecutive
        ['>', '>', '>', 'O', 'O', 'O'],  # Three consecutive at start
        ['O', '>', 'O', '>', '>', '>'],  # Three consecutive at end
    ]
    
    print("Testing fixed _check_sequence method:")
    for i, test in enumerate(test_cases):
        print(f"\nTest {i+1}: {test}")
        result = solver.debug_check_sequence(test)
        print(f"Result: {'Valid' if result else 'Invalid'}")
    
    # Test the specific case from the bug
    print("\nTesting the specific case from the bug:")
    column_6 = ['O', None, None, '>', None, '>']
    print("Column 6 with None values preserved:")
    result = solver.debug_check_sequence(column_6)
    print(f"Result: {'Valid' if result else 'Invalid'}")
    
    # Test with the proposed value
    column_6_with_value = ['O', '>', None, '>', None, '>']
    print("\nColumn 6 with '>' at position 2:")
    result = solver.debug_check_sequence(column_6_with_value)
    print(f"Result: {'Valid' if result else 'Invalid'}")
    
    # Compare with the old method
    print("\nComparing with the original method:")
    original_solver = BinaryPuzzleCSP()
    
    # Filter out None values (as in the original method)
    filtered_column_6 = [v for v in column_6 if v is not None]
    print(f"Original column 6 after filtering None values: {filtered_column_6}")
    result = original_solver._check_sequence(filtered_column_6)
    print(f"Original method result: {'Valid' if result else 'Invalid'}")
    
    filtered_column_6_with_value = [v for v in column_6_with_value if v is not None]
    print(f"Column 6 with value after filtering None values: {filtered_column_6_with_value}")
    result = original_solver._check_sequence(filtered_column_6_with_value)
    print(f"Original method result: {'Valid' if result else 'Invalid'}")
    
    print("\nConclusion:")
    print("The bug is in the _check_sequence method. By filtering out None values before checking,")
    print("it incorrectly treats non-consecutive symbols as consecutive, leading to false negatives.")
    print("The fixed version properly handles None values and only counts consecutive positions.")

if __name__ == "__main__":
    main()