def parse_input(input_text):
    """
    Parse the input to get red tile positions.
    
    Args:
        input_text: String with one position per line in format "x,y"
    
    Returns:
        List of (x, y) tuples representing red tile positions
    """
    positions = []
    for line in input_text.strip().split('\n'):
        x, y = map(int, line.split(','))
        positions.append((x, y))
    return positions


def point_in_polygon(point, polygon):
    """
    Check if a point is inside or on the boundary of a polygon using ray casting algorithm.
    
    The polygon is formed by connecting consecutive points in the list, wrapping around.
    This implements:
    1. Edge checking: Test if point lies on any polygon edge
    2. Ray casting: Cast a ray from the point and count edge crossings
    
    Args:
        point: (x, y) tuple to test
        polygon: list of (x, y) tuples forming the polygon vertices in order
    
    Returns:
        True if point is inside or on the polygon boundary, False otherwise
    """
    x, y = point
    n = len(polygon)
    inside = False
    
    # First pass: Check if point is on any edge of the polygon
    for i in range(n):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % n]  # Wrap around to close the polygon
        
        # Check if point is within the bounding box of this edge
        if min(x1, x2) <= x <= max(x1, x2) and min(y1, y2) <= y <= max(y1, y2):
            # Use cross product to check if point is collinear with the edge
            cross = (y - y1) * (x2 - x1) - (x - x1) * (y2 - y1)
            if cross == 0:  # Point is on the edge
                return True
    
    # Second pass: Ray casting algorithm for interior points
    # Cast a horizontal ray from the point to the right and count intersections
    p1x, p1y = polygon[0]
    for i in range(1, n + 1):
        p2x, p2y = polygon[i % n]
        # Check if the ray crosses this edge
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        # Calculate x coordinate of intersection
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside  # Toggle inside/outside status
        p1x, p1y = p2x, p2y
    
    return inside


def solve(input_text):
    """
    Part 1: Find the largest rectangle using two red tiles as opposite corners.
    
    This is straightforward - try all pairs of red tiles and calculate the
    rectangle area between them. No constraints on what tiles the rectangle
    can include.
    
    Algorithm:
    - Iterate through all pairs of red tiles (O(n²) where n is number of tiles)
    - For each pair, treat them as opposite corners of an axis-aligned rectangle
    - Calculate area as (width + 1) × (height + 1) to include boundaries
    - Track and return the maximum area found
    
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
            
            # Calculate rectangle dimensions (inclusive of both corner tiles)
            # Add 1 because we count the tiles at both boundaries
            width = abs(x2 - x1) + 1
            height = abs(y2 - y1) + 1
            
            # Calculate and track maximum area
            area = width * height
            max_area = max(max_area, area)
    
    return max_area


def rectangle_valid_in_polygon(min_x, max_x, min_y, max_y, positions):
    """
    Check if a rectangle is completely inside the polygon.
    
    This is more stringent than just checking corners - we need to verify that
    the rectangle edges don't cross outside the polygon boundary. For non-convex
    polygons, corners can be inside while edges bulge outside.
    
    Strategy: Sample points along the rectangle perimeter at regular intervals.
    If all sampled points are inside/on the polygon, the rectangle is valid.
    
    Args:
        min_x, max_x: X bounds of rectangle (inclusive)
        min_y, max_y: Y bounds of rectangle (inclusive)
        positions: List of polygon vertices
    
    Returns:
        True if the entire rectangle is contained within the polygon
    """
    # Define the four corners
    corners = [
        (min_x, min_y),
        (min_x, max_y),
        (max_x, min_y),
        (max_x, max_y)
    ]
    
    # First check: all corners must be inside/on polygon
    for corner in corners:
        if not point_in_polygon(corner, positions):
            return False
    
    # Second check: sample points along each edge
    # We need dense enough sampling to catch cases where edges cross outside
    sample_points = []
    
    # Sample horizontal edges (top and bottom)
    width = max_x - min_x
    # Sample every 100 units, or divide into at least 20 segments
    step_x = max(1, min(100, width // 20))
    for x in range(min_x, max_x + 1, step_x):
        sample_points.append((x, min_y))  # Bottom edge
        sample_points.append((x, max_y))  # Top edge
    
    # Sample vertical edges (left and right)
    height = max_y - min_y
    step_y = max(1, min(100, height // 20))
    for y in range(min_y, max_y + 1, step_y):
        sample_points.append((min_x, y))  # Left edge
        sample_points.append((max_x, y))  # Right edge
    
    # Verify all sampled points are inside the polygon
    for point in sample_points:
        if not point_in_polygon(point, positions):
            return False
    
    return True


def solve_part2(input_text):
    """
    Part 2: Find the largest rectangle using two red tiles as opposite corners,
    where ALL tiles in the rectangle must be red or green.
    
    Green tiles are defined as:
    1. Tiles on the edges connecting consecutive red tiles (forming a polygon)
    2. All tiles inside this polygon
    
    The key challenge: For non-convex polygons, a rectangle with corners inside
    can still have edges that cross outside. We must verify the entire rectangle
    boundary stays within the polygon.
    
    Algorithm:
    - Try all pairs of red tiles as potential rectangle corners
    - For each pair, check if the rectangle is completely contained in the polygon
    - Use edge sampling to verify containment (checking just corners isn't sufficient)
    - Track the maximum valid rectangle area
    
    Args:
        input_text: Input containing red tile positions in order
    
    Returns:
        Maximum valid rectangle area
    """
    positions = parse_input(input_text)
    n = len(positions)
    
    print(f"Part 2: Processing {n} red tiles...")
    print(f"Total pairs to check: {n * (n - 1) // 2}")
    
    max_area = 0
    pairs_checked = 0
    total_pairs = n * (n - 1) // 2
    
    # Try all pairs of red tiles as opposite corners
    for i in range(n):
        # Progress reporting every 50 tiles
        if i % 50 == 0:
            print(f"Progress: tile {i}/{n}, {pairs_checked}/{total_pairs} pairs checked, max area: {max_area}")
        
        for j in range(i + 1, n):
            pairs_checked += 1
            
            x1, y1 = positions[i]
            x2, y2 = positions[j]
            
            # Calculate rectangle dimensions (inclusive of both corners)
            width = abs(x2 - x1) + 1
            height = abs(y2 - y1) + 1
            area = width * height
            
            # Early termination: skip if this rectangle can't beat current best
            if area <= max_area:
                continue
            
            # Get the bounding box of the rectangle
            min_x, max_x = min(x1, x2), max(x1, x2)
            min_y, max_y = min(y1, y2), max(y1, y2)
            
            # Check if rectangle is valid (fully contained in polygon)
            if rectangle_valid_in_polygon(min_x, max_x, min_y, max_y, positions):
                max_area = area
    
    print(f"Final: checked {pairs_checked} pairs, max area: {max_area}")
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

print("Example Part 2:")
result2 = solve_part2(example)
print(f"Largest rectangle area (red/green only): {result2}")
print(f"Expected: 24")
print()

# Solve the actual puzzle
import os
for filename in ['input.txt', 'input']:
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            puzzle_input = f.read()
        print("Puzzle Part 1:")
        answer = solve(puzzle_input)
        print(f"Largest rectangle area: {answer}")
        print()
        print("Puzzle Part 2:")
        answer2 = solve_part2(puzzle_input)
        print(f"Largest rectangle area (red/green only): {answer2}")
        break
else:
    print("No input file found.")
