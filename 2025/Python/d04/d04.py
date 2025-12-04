# Directions for the 8 adjacent positions (including diagonals)
DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),  # top-left, top, top-right
    (0, -1),           (0, 1),    # left, right
    (1, -1),  (1, 0),  (1, 1)     # bottom-left, bottom, bottom-right
]


def count_accessible_rolls(grid):
    """
    Count the number of rolls of paper that can be accessed by a forklift.
    A roll can be accessed if there are fewer than 4 rolls in the 8 adjacent positions.
    
    Args:
        grid: List of strings representing the grid
    
    Returns:
        The number of rolls that can be accessed
    """
    if not grid:
        return 0
    
    rows = len(grid)
    cols = len(grid[0])
    accessible_count = 0
    
    # Check each position in the grid
    for row in range(rows):
        for col in range(cols):
            # Only check positions that have a roll of paper
            if grid[row][col] == '@':
                # Count adjacent rolls
                adjacent_rolls = 0
                
                for dr, dc in DIRECTIONS:
                    new_row = row + dr
                    new_col = col + dc
                    
                    # Check if the position is within bounds
                    if 0 <= new_row < rows and 0 <= new_col < cols:
                        if grid[new_row][new_col] == '@':
                            adjacent_rolls += 1
                
                # A roll can be accessed if there are fewer than 4 adjacent rolls
                if adjacent_rolls < 4:
                    accessible_count += 1
    
    return accessible_count


def count_removable_rolls(grid):
    """
    Count the total number of rolls that can be removed by repeatedly
    removing accessible rolls until no more can be removed.
    
    Args:
        grid: List of strings representing the grid
    
    Returns:
        The total number of rolls that can be removed
    """
    if not grid:
        return 0
    
    # Create a mutable copy of the grid (convert strings to lists)
    mutable_grid = [list(row) for row in grid]
    rows = len(mutable_grid)
    cols = len(mutable_grid[0])
    
    total_removed = 0
    
    # Keep removing accessible rolls until none can be removed
    while True:
        # Find all accessible rolls in this iteration
        accessible_positions = []
        
        for row in range(rows):
            for col in range(cols):
                # Only check positions that have a roll of paper
                if mutable_grid[row][col] == '@':
                    # Count adjacent rolls
                    adjacent_rolls = 0
                    
                    for dr, dc in DIRECTIONS:
                        new_row = row + dr
                        new_col = col + dc
                        
                        # Check if the position is within bounds
                        if 0 <= new_row < rows and 0 <= new_col < cols:
                            if mutable_grid[new_row][new_col] == '@':
                                adjacent_rolls += 1
                    
                    # A roll can be accessed if there are fewer than 4 adjacent rolls
                    if adjacent_rolls < 4:
                        accessible_positions.append((row, col))
        
        # If no accessible rolls found, we're done
        if not accessible_positions:
            break
        
        # Remove all accessible rolls
        for row, col in accessible_positions:
            mutable_grid[row][col] = '.'
        
        # Add to total count
        total_removed += len(accessible_positions)
    
    return total_removed


def solve(input_text):
    """
    Parse the input and count accessible rolls.
    
    Args:
        input_text: Multi-line string representing the grid
    
    Returns:
        The number of rolls that can be accessed
    """
    grid = [line.strip() for line in input_text.strip().split('\n') if line.strip()]
    return count_accessible_rolls(grid)


def solve_part2(input_text):
    """
    Parse the input and count total removable rolls.
    
    Args:
        input_text: Multi-line string representing the grid
    
    Returns:
        The total number of rolls that can be removed
    """
    grid = [line.strip() for line in input_text.strip().split('\n') if line.strip()]
    return count_removable_rolls(grid)


# Test with the example from the puzzle description
example = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""

print("Example (Part 1):")
result = solve(example)
print(f"Number of accessible rolls: {result}")
print(f"Expected: 13")
print()

print("Example (Part 2):")
result_part2 = solve_part2(example)
print(f"Total removable rolls: {result_part2}")
print(f"Expected: 43")
print()

# Solve the actual puzzle
import os
for filename in ['input.txt', 'input']:
    filepath = os.path.join(os.path.dirname(__file__), filename)
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            puzzle_input = f.read()
        print("Part 1 answer:")
        answer = solve(puzzle_input)
        print(f"Number of accessible rolls: {answer}")
        print()
        print("Part 2 answer:")
        answer_part2 = solve_part2(puzzle_input)
        print(f"Total removable rolls: {answer_part2}")
        break
else:
    print("No input file found.")
