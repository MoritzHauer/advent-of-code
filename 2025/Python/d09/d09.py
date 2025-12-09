def parse_input(input_text):
    """Parse the input to get red tile positions."""
    positions = []
    for line in input_text.strip().split('\n'):
        x, y = map(int, line.split(','))
        positions.append((x, y))
    return positions


def solve(input_text):
    """
    Find the largest rectangle using two red tiles as opposite corners.
    
    Args:
        input_text: Input containing red tile positions
    
    Returns:
        Maximum rectangle area
    """
    positions = parse_input(input_text)
    n = len(positions)
    
    max_area = 0
    
    # Try all pairs of red tiles as opposite corners
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = positions[i]
            x2, y2 = positions[j]
            
            # Calculate rectangle dimensions (inclusive of both corners)
            width = abs(x2 - x1) + 1
            height = abs(y2 - y1) + 1
            
            # Calculate area
            area = width * height
            
            max_area = max(max_area, area)
    
    return max_area


# Test with the example
example = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""

print("Example:")
result = solve(example)
print(f"Largest rectangle area: {result}")
print(f"Expected: 50")
print()

# Solve the actual puzzle
import os
for filename in ['input.txt', 'input']:
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            puzzle_input = f.read()
        print("Puzzle answer:")
        answer = solve(puzzle_input)
        print(f"Largest rectangle area: {answer}")
        break
else:
    print("No input file found.")
