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


def simulate_quantum_beams(grid, start_pos):
    """
    Simulate quantum tachyon beams through the manifold.
    
    In quantum mode, each particle takes BOTH paths at each splitter.
    We count the number of distinct paths by tracking multiplicities.
    
    Args:
        grid: 2D list representing the manifold
        start_pos: Starting position (row, col) of the particle
    
    Returns:
        Number of different timelines
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    
    # Track beams: dict mapping (row, col) -> number of distinct paths
    beams = {(start_pos[0], start_pos[1]): 1}
    completed_count = 0
    
    iteration = 0
    while beams:
        iteration += 1
        if iteration % 100 == 0:
            print(f"Iteration {iteration}, active beams: {len(beams)}, completed: {completed_count}")
        
        new_beams = {}
        
        for (row, col), path_count in beams.items():
            # Move beam down one step
            next_row = row + 1
            
            # Check if beam exits
            if next_row >= rows:
                completed_count += path_count
                continue
            
            # Check what's at next position
            cell = grid[next_row][col]
            
            if cell == '^':
                # Splitter - both paths
                left_col = col - 1
                if left_col >= 0:
                    pos = (next_row, left_col)
                    new_beams[pos] = new_beams.get(pos, 0) + path_count
                else:
                    completed_count += path_count
                
                right_col = col + 1
                if right_col < cols:
                    pos = (next_row, right_col)
                    new_beams[pos] = new_beams.get(pos, 0) + path_count
                else:
                    completed_count += path_count
            else:
                # Continue downward
                pos = (next_row, col)
                new_beams[pos] = new_beams.get(pos, 0) + path_count
        
        beams = new_beams
    
    print(f"Final: {completed_count} timelines")
    return completed_count


def solve(input_text, quantum_mode=False):
    """
    Count beam splits (part 1) or timelines (part 2).
    
    Args:
        input_text: The manifold diagram
        quantum_mode: If True, count timelines; otherwise count splits
    
    Returns:
        Number of splits or timelines
    """
    grid, start_pos = parse_manifold(input_text)
    
    if quantum_mode:
        return simulate_quantum_beams(grid, start_pos)
    else:
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

print("Part 1 Example:")
result = solve(example)
print(f"Beam splits: {result}")
print(f"Expected: 21")
print()

print("Part 2 Example:")
result2 = solve(example, quantum_mode=True)
print(f"Timelines: {result2}")
print(f"Expected: 40")
print()

# Solve the actual puzzle
import os
for filename in ['input.txt', 'input']:
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            puzzle_input = f.read()
        print("Part 1 Puzzle answer:")
        answer1 = solve(puzzle_input)
        print(f"Beam splits: {answer1}")
        print()
        print("Part 2 Puzzle answer:")
        answer2 = solve(puzzle_input, quantum_mode=True)
        print(f"Timelines: {answer2}")
        break
else:
    print("No input file found.")
