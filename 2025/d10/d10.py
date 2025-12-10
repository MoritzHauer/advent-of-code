import re
from typing import List, Tuple

def parse_line(line: str) -> Tuple[List[bool], List[List[int]], List[int]]:
    """Parse a machine line into target state, button configurations, and joltage requirements."""
    # Extract the target pattern [.##.]
    target_match = re.search(r'\[([.#]+)\]', line)
    target = [c == '#' for c in target_match.group(1)]
    
    # Extract all button configurations (1,2,3)
    buttons = []
    for match in re.finditer(r'\(([0-9,]+)\)', line):
        button = [int(x) for x in match.group(1).split(',')]
        buttons.append(button)
    
    # Extract joltage requirements {3,5,4,7}
    joltage_match = re.search(r'\{([0-9,]+)\}', line)
    joltage = [int(x) for x in joltage_match.group(1).split(',')]
    
    return target, buttons, joltage

def solve_machine(target: List[bool], buttons: List[List[int]]) -> int:
    """
    Solve one machine using Gaussian elimination over GF(2).
    Returns minimum button presses needed.
    
    This is a system of linear equations over GF(2) where:
    - Each row represents a light
    - Each column represents a button
    - Matrix[i][j] = 1 if button j toggles light i
    - We want to find button press counts (mod 2) that achieve target
    """
    n_lights = len(target)
    n_buttons = len(buttons)
    
    # Build augmented matrix [A | b] where A is button effects, b is target
    # Each row is a light, each column is a button
    matrix = []
    for light_idx in range(n_lights):
        row = []
        # Check which buttons affect this light
        for button in buttons:
            row.append(1 if light_idx in button else 0)
        # Add target state for this light
        row.append(1 if target[light_idx] else 0)
        matrix.append(row)
    
    # Gaussian elimination over GF(2)
    # Keep track of which columns are pivot columns
    pivot_cols = []
    current_row = 0
    
    for col in range(n_buttons):
        # Find pivot
        pivot_row = None
        for row in range(current_row, n_lights):
            if matrix[row][col] == 1:
                pivot_row = row
                break
        
        if pivot_row is None:
            continue
        
        pivot_cols.append(col)
        
        # Swap rows
        matrix[current_row], matrix[pivot_row] = matrix[pivot_row], matrix[current_row]
        
        # Eliminate other rows
        for row in range(n_lights):
            if row != current_row and matrix[row][col] == 1:
                # XOR rows (addition in GF(2))
                for c in range(n_buttons + 1):
                    matrix[row][c] ^= matrix[current_row][c]
        
        current_row += 1
    
    # Check if solution exists
    for row in range(current_row, n_lights):
        if matrix[row][n_buttons] == 1:
            # Inconsistent system - no solution
            return float('inf')
    
    # Find free variables (non-pivot columns)
    free_vars = [col for col in range(n_buttons) if col not in pivot_cols]
    
    # Try all combinations of free variables to find minimum
    min_presses = float('inf')
    
    for mask in range(1 << len(free_vars)):
        button_presses = [0] * n_buttons
        
        # Set free variables based on mask
        for i, col in enumerate(free_vars):
            button_presses[col] = (mask >> i) & 1
        
        # Back substitution for pivot variables
        for row in range(len(pivot_cols) - 1, -1, -1):
            col = pivot_cols[row]
            
            # Calculate value for this button
            value = matrix[row][n_buttons]
            for c in range(col + 1, n_buttons):
                value ^= (matrix[row][c] * button_presses[c])
            
            button_presses[col] = value
        
        # Count total presses for this combination
        presses = sum(button_presses)
        min_presses = min(min_presses, presses)
    
    return min_presses


def solve_machine_part2(joltage_target: List[int], buttons: List[List[int]]) -> int:
    """
    Solve Part 2: Find minimum button presses to reach joltage targets.
    
    This is a system of linear equations over integers:
    - Each counter needs to reach a specific joltage value
    - Each button press increments specific counters by 1
    - We need to find non-negative integer button press counts that minimize total presses
    
    This is essentially finding the minimum L1 norm solution to Ax = b where x >= 0.
    We can use linear programming or try a greedy/optimization approach.
    """
    n_counters = len(joltage_target)
    n_buttons = len(buttons)
    
    # Build the coefficient matrix
    # matrix[i][j] = 1 if button j affects counter i
    matrix = []
    for counter_idx in range(n_counters):
        row = []
        for button in buttons:
            row.append(1 if counter_idx in button else 0)
        matrix.append(row)
    
    # Try to solve using a greedy approach with linear programming
    # We want to minimize sum(x_i) subject to A*x = b and x >= 0
    
    try:
        from scipy.optimize import linprog
        
        # Objective: minimize sum of all button presses (all coefficients are 1)
        c = [1] * n_buttons
        
        # Equality constraint: A*x = b (each counter must reach target)
        A_eq = matrix
        b_eq = joltage_target
        
        # Bounds: each button can be pressed 0 or more times
        bounds = [(0, None) for _ in range(n_buttons)]
        
        result = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')
        
        if result.success:
            # Round the solution to integers and verify
            solution = [round(x) for x in result.x]
            
            # Verify the solution works
            achieved = [0] * n_counters
            for button_idx, presses in enumerate(solution):
                for counter in buttons[button_idx]:
                    achieved[counter] += presses
            
            if achieved == joltage_target:
                return sum(solution)
            
            # If rounding didn't work, try integer programming
            from scipy.optimize import milp, LinearConstraint, Bounds
            
            # Integer programming
            integrality = [1] * n_buttons  # All variables must be integers
            
            constraints = LinearConstraint(A_eq, b_eq, b_eq)
            bounds_obj = Bounds(lb=[0]*n_buttons, ub=[max(joltage_target)*2]*n_buttons)
            
            result = milp(c=c, constraints=constraints, bounds=bounds_obj, integrality=integrality)
            
            if result.success:
                return int(sum(result.x))
    
    except ImportError:
        pass
    
    # Fallback: simple greedy approach if scipy not available
    # Try to find a solution by trying different combinations
    # For small problems, we can try systematic search
    
    # Use a simple backtracking approach for small problems
    def can_reach_target(current, remaining_target, button_idx, presses_used):
        if button_idx == n_buttons:
            return sum(presses_used) if all(r == 0 for r in remaining_target) else float('inf')
        
        min_presses = float('inf')
        
        # Calculate max useful presses for this button
        max_presses = 0
        for counter in buttons[button_idx]:
            if counter < n_counters:
                max_presses = max(max_presses, remaining_target[counter])
        
        # Try different numbers of presses for this button
        for presses in range(max_presses + 1):
            new_remaining = remaining_target[:]
            valid = True
            
            for counter in buttons[button_idx]:
                if counter < n_counters:
                    new_remaining[counter] -= presses
                    if new_remaining[counter] < 0:
                        valid = False
                        break
            
            if valid:
                result = can_reach_target(current, new_remaining, button_idx + 1, presses_used + [presses])
                min_presses = min(min_presses, result)
        
        return min_presses
    
    result = can_reach_target([0] * n_counters, joltage_target[:], 0, [])
    return result if result != float('inf') else 0

def solve_part1(filename: str) -> int:
    """Solve part 1 - find minimum button presses for all machines."""
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    total_presses = 0
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        target, buttons = parse_line(line)
        presses = solve_machine(target, buttons)
        total_presses += presses
    
    return total_presses

# Test with example
example = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""

# Test each example machine
total = 0
for i, line in enumerate(example.split('\n'), 1):
    target, buttons = parse_line(line)
    presses = solve_machine(target, buttons)
    print(f"Machine {i}: target={['#' if t else '.' for t in target]}, buttons={buttons}")
    print(f"  -> needs {presses} button presses")
    total += presses

print(f"\nExample total: {total} (expected 7)")

# Solve actual puzzle
result = solve_part1('input')
print(f"\nPart 1 answer: {result}")