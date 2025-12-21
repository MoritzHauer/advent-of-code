#!/usr/bin/env python3
"""
Day 12: Christmas Tree Farm - Polyomino packing problem

We need to fit polyominoes (present shapes) into rectangular regions.
- Shapes can be rotated and flipped
- Shapes can't overlap (# parts)
- . parts don't block other shapes

Strategy:
1. Parse shapes and generate all rotations/flips
2. For each region, use backtracking to try placing all presents
3. Count how many regions can fit all their presents
"""

from typing import List, Set, Tuple
from copy import deepcopy


def parse_input(filename: str):
    """Parse the input file to extract shapes and regions."""
    with open(filename, 'r') as f:
        content = f.read().strip()
    
    sections = content.split('\n\n')
    
    # Parse shapes
    shapes = {}
    i = 0
    while i < len(sections):
        lines = sections[i].strip().split('\n')
        if ':' in lines[0] and 'x' not in lines[0]:
            # This is a shape definition
            shape_id = int(lines[0].rstrip(':'))
            shape_lines = lines[1:]
            shape = []
            for line in shape_lines:
                shape.append(list(line))
            shapes[shape_id] = shape
            i += 1
        else:
            break
    
    # Parse regions
    regions = []
    for j in range(i, len(sections)):
        lines = sections[j].strip().split('\n')
        for line in lines:
            if 'x' in line:
                parts = line.split(': ')
                dims = parts[0].split('x')
                width, height = int(dims[0]), int(dims[1])
                counts = list(map(int, parts[1].split()))
                regions.append((width, height, counts))
    
    return shapes, regions


def get_shape_coords(shape: List[List[str]]) -> Set[Tuple[int, int]]:
    """Extract coordinates of # cells in a shape."""
    coords = set()
    for r in range(len(shape)):
        for c in range(len(shape[0])):
            if shape[r][c] == '#':
                coords.add((r, c))
    return coords


def normalize_coords(coords: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
    """Normalize coordinates so the minimum r and c are 0."""
    if not coords:
        return coords
    min_r = min(r for r, c in coords)
    min_c = min(c for r, c in coords)
    return {(r - min_r, c - min_c) for r, c in coords}


def rotate_90(coords: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
    """Rotate coordinates 90 degrees clockwise."""
    return normalize_coords({(c, -r) for r, c in coords})


def flip_horizontal(coords: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
    """Flip coordinates horizontally."""
    return normalize_coords({(r, -c) for r, c in coords})


def get_all_orientations(shape: List[List[str]]) -> List[Set[Tuple[int, int]]]:
    """Generate all unique rotations and flips of a shape."""
    coords = get_shape_coords(shape)
    coords = normalize_coords(coords)
    
    orientations = set()
    current = coords
    
    # 4 rotations
    for _ in range(4):
        orientations.add(frozenset(current))
        current = rotate_90(current)
    
    # Flip and 4 more rotations
    current = flip_horizontal(coords)
    for _ in range(4):
        orientations.add(frozenset(current))
        current = rotate_90(current)
    
    return [set(o) for o in orientations]


def can_place(grid: List[List[bool]], coords: Set[Tuple[int, int]], 
              r_offset: int, c_offset: int, width: int, height: int) -> bool:
    """Check if a shape can be placed at the given offset."""
    for r, c in coords:
        new_r, new_c = r + r_offset, c + c_offset
        if new_r < 0 or new_r >= height or new_c < 0 or new_c >= width:
            return False
        if grid[new_r][new_c]:
            return False
    return True


def place_shape(grid: List[List[bool]], coords: Set[Tuple[int, int]], 
                r_offset: int, c_offset: int):
    """Place a shape on the grid."""
    for r, c in coords:
        grid[r + r_offset][c + c_offset] = True


def remove_shape(grid: List[List[bool]], coords: Set[Tuple[int, int]], 
                 r_offset: int, c_offset: int):
    """Remove a shape from the grid."""
    for r, c in coords:
        grid[r + r_offset][c + c_offset] = False


def solve_region(shapes: dict, width: int, height: int, counts: List[int]) -> bool:
    """
    Try to fit all presents into the region using backtracking with optimizations.
    Returns True if all presents can be fitted.
    """
    # Create list of presents to place
    presents = []
    for shape_id, count in enumerate(counts):
        for _ in range(count):
            presents.append(shape_id)
    
    if not presents:
        return True
    
    # Quick check: total area
    total_shape_area = sum(
        len(get_shape_coords(shapes[shape_id])) 
        for shape_id in presents
    )
    grid_area = width * height
    if total_shape_area > grid_area:
        return False
    
    # Pre-compute all orientations for each shape
    shape_orientations = {}
    for shape_id in shapes:
        shape_orientations[shape_id] = get_all_orientations(shapes[shape_id])
    
    # Initialize empty grid
    grid = [[False] * width for _ in range(height)]
    
    def find_first_empty() -> Tuple[int, int]:
        """Find the first empty cell (top-left scanning)."""
        for r in range(height):
            for c in range(width):
                if not grid[r][c]:
                    return (r, c)
        return None
    
    def backtrack(present_idx: int) -> bool:
        if present_idx == len(presents):
            return True
        
        # Find first empty position
        pos = find_first_empty()
        if pos is None:
            return present_idx == len(presents)
        
        r_target, c_target = pos
        shape_id = presents[present_idx]
        
        # Try each orientation
        for orientation in shape_orientations[shape_id]:
            # For this orientation, try positions where the shape covers (r_target, c_target)
            for dr, dc in orientation:
                r_offset = r_target - dr
                c_offset = c_target - dc
                
                if can_place(grid, orientation, r_offset, c_offset, width, height):
                    place_shape(grid, orientation, r_offset, c_offset)
                    
                    if backtrack(present_idx + 1):
                        return True
                    
                    remove_shape(grid, orientation, r_offset, c_offset)
        
        return False
    
    return backtrack(0)


def solve_part1(filename: str) -> int:
    """Count how many regions can fit all their presents."""
    shapes, regions = parse_input(filename)
    
    # Check area of each shape
    print("Shape areas:")
    for shape_id in sorted(shapes.keys()):
        coords = get_shape_coords(shapes[shape_id])
        print(f"  Shape {shape_id}: {len(coords)} cells")
    
    count = 0
    for i, (width, height, counts) in enumerate(regions):
        total_shape_area = sum(
            len(get_shape_coords(shapes[shape_id])) * count
            for shape_id, count in enumerate(counts)
        )
        grid_area = width * height
        
        print(f"Region {i+1}: {width}x{height} = {grid_area} cells, needs {total_shape_area} cells for {sum(counts)} presents")
        
        if total_shape_area <= grid_area:
            # Do actual packing test only if area check passes
            if solve_region(shapes, width, height, counts):
                count += 1
                print(f"  ✓ Can fit")
            else:
                print(f"  ✗ Cannot fit (area OK but packing failed)")
        else:
            print(f"  ✗ Cannot fit (not enough area)")
    
    return count


# Test with example
example_input = """0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2"""

with open('example', 'w') as f:
    f.write(example_input)

print("=== Part 1 ===")
print("Testing example...")
example_result = solve_part1('example')
print(f"\nExample: {example_result} regions can fit (expected 2)\n")

print("Solving actual puzzle...")
result = solve_part1('input')
print(f"\nPart 1 answer: {result}")
