def solve_safe_password(rotations):
    """
    Calculate the password by counting how many times the dial points at 0.
    
    Args:
        rotations: List of rotation instructions (e.g., ["L68", "R48"])
    
    Returns:
        The number of times the dial points at 0
    """
    position = 50  # Starting position
    count = 0
    
    for rotation in rotations:
        direction = rotation[0]
        distance = int(rotation[1:])
        
        if direction == 'L':
            position = (position - distance) % 100
        else:  # direction == 'R'
            position = (position + distance) % 100
        
        if position == 0:
            count += 1
    
    return count


# Example test case
example_rotations = [
    "L68", "L30", "R48", "L5", "R60",
    "L55", "L1", "L99", "R14", "L82"
]

print("Example result:", solve_safe_password(example_rotations))
print("Expected: 3")

# Try to load and solve the actual puzzle input if it exists
import os
for filename in ['input.txt', 'input']:
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            puzzle_rotations = [line.strip() for line in f if line.strip()]
        print(f"\nPuzzle answer: {solve_safe_password(puzzle_rotations)}")
        break
else:
    print("\nNo input file found. Add your puzzle input to solve the actual puzzle.")
