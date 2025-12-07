def parse_manifold(input_text):
    """
    Parse the tachyon manifold diagram.
    
    Args:
        input_text: Multi-line string representing the manifold
    
    Returns:
        Tuple of (grid, start_pos) where grid is a 2D list and start_pos is (row, col)
    """
    lines = input_text.strip().split('\n')
    grid = [list(line) for line in lines]
    
    # Find starting position (S)
    start_pos = None
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == 'S':
                start_pos = (row, col)
                break
        if start_pos:
            break
    
    return grid, start_pos


def simulate_beams(grid, start_pos):
    """
    Simulate the tachyon beams through the manifold.
    
    Tachyon beams always move downward. When a beam hits a splitter (^),
    it stops and creates two new beams starting from the immediate left
    and immediate right of the splitter, both moving downward.
    
    Args:
        grid: 2D list representing the manifold
        start_pos: Starting position (row, col) of the initial beam
    
    Returns:
        Number of times beams are split (number of unique splitters hit)
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    
    # Track beams: list of (row, col) tuples (all beams move downward)
    beams = [(start_pos[0], start_pos[1])]
    
    # Track which (row, col) positions have already processed beams
    processed_beams = set()
    
    # Track which splitters have been hit
    hit_splitters = set()
    
    while beams:
        new_beams = []
        
        for row, col in beams:
            # Skip if we've already processed a beam from this position
            if (row, col) in processed_beams:
                continue
            processed_beams.add((row, col))
            
            # Move beam down until it hits a splitter or exits
            current_row = row
            
            while True:
                next_row = current_row + 1
                
                # Check if beam exits the manifold
                if next_row >= rows:
                    break
                
                # Check what's at the next position
                cell = grid[next_row][col]
                
                if cell == '^':
                    # Hit a splitter
                    hit_splitters.add((next_row, col))
                    
                    # Create two new beams starting from positions to the left and right
                    # of the splitter, both moving downward
                    left_col = col - 1
                    right_col = col + 1
                    
                    if left_col >= 0 and (next_row, left_col) not in processed_beams:
                        new_beams.append((next_row, left_col))
                    
                    if right_col < cols and (next_row, right_col) not in processed_beams:
                        new_beams.append((next_row, right_col))
                    
                    break
                else:
                    # Empty space or start - beam continues downward
                    current_row = next_row
        
        beams = new_beams
    
    return len(hit_splitters)


def solve(input_text):
    """
    Count how many times the tachyon beam is split.
    
    Args:
        input_text: The manifold diagram
    
    Returns:
        Number of beam splits
    """
    grid, start_pos = parse_manifold(input_text)
    return simulate_beams(grid, start_pos)


# Test with the example
example = """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
..............."""

print("Example:")
result = solve(example)
print(f"Beam splits: {result}")
print(f"Expected: 21")
print()

# Solve the actual puzzle
import os
for filename in ['input.txt', 'input']:
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            puzzle_input = f.read()
        print("Puzzle answer:")
        answer = solve(puzzle_input)
        print(f"Beam splits: {answer}")
        break
else:
    print("No input file found.")
