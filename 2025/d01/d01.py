def solve_safe_password(rotations, count_clicks=False):
    """
    Calculate the password by counting how many times the dial points at 0.
    
    Args:
        rotations: List of rotation instructions (e.g., ["L68", "R48"])
        count_clicks: If True, count every time dial passes 0 during rotation,
                     not just when it ends on 0
    
    Returns:
        The number of times the dial points at 0
    """
    position = 50  # Starting position
    count = 0
    
    for rotation in rotations:
        direction = rotation[0]
        distance = int(rotation[1:])
        
        if count_clicks:
            # Count how many times we click on 0 during the rotation
            # We click on positions: current+1, current+2, ..., current+distance (for R)
            # or current-1, current-2, ..., current-distance (for L)
            # We need to count how many of these positions equal 0 (mod 100)
            
            # How many complete loops of 100?
            full_loops = distance // 100
            count += full_loops
            
            # For the remaining partial rotation, check if we hit 0
            remainder = distance % 100
            if direction == 'L':
                # Going left from position by remainder clicks
                # We hit 0 if position - k = 0 (mod 100) for some k in [1, remainder]
                # This means k = position (mod 100)
                # Since position is already in [0, 99], we hit 0 if position <= remainder and position > 0
                if position > 0 and position <= remainder:
                    count += 1
            else:  # direction == 'R'
                # Going right from position by remainder clicks
                # We hit 0 if position + k = 0 (mod 100) for some k in [1, remainder]
                # This means position + k = 100, so k = 100 - position
                # We hit 0 if 100 - position is in [1, remainder]
                if position + remainder >= 100:
                    count += 1
        
        # Move to new position
        if direction == 'L':
            position = (position - distance) % 100
        else:  # direction == 'R'
            position = (position + distance) % 100
        
        # Count if we end exactly on 0 (only for part 1)
        if not count_clicks and position == 0:
            count += 1
    
    return count


# Example test case
example_rotations = [
    "L68", "L30", "R48", "L5", "R60",
    "L55", "L1", "L99", "R14", "L82"
]

print("Example result:", solve_safe_password(example_rotations))
print("Expected: 3")

print("\nPart 2 Example result:", solve_safe_password(example_rotations, count_clicks=True))
print("Expected: 6")

# Try to load and solve the actual puzzle input if it exists
import os
for filename in ['input.txt', 'input']:
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            puzzle_rotations = [line.strip() for line in f if line.strip()]
        print(f"\nPart 1 answer: {solve_safe_password(puzzle_rotations)}")
        print(f"Part 2 answer: {solve_safe_password(puzzle_rotations, count_clicks=True)}")
        break
else:
    print("\nNo input file found. Add your puzzle input to solve the actual puzzle.")
