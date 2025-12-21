#!/usr/bin/env python3
"""
Day 12: Test if it's just an area check problem
"""

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


def get_shape_area(shape):
    """Count # cells in a shape."""
    count = 0
    for row in shape:
        count += row.count('#')
    return count


# Simple hypothesis: a region can fit if area(region) >= total area of all presents
shapes, regions = parse_input('input')

print("Shape areas:")
for sid in sorted(shapes.keys()):
    area = get_shape_area(shapes[sid])
    print(f"  Shape {sid}: {area} cells")

print("\nChecking regions (simple area test):")
count_area_only = 0
for i, (width, height, counts) in enumerate(regions):
    grid_area = width * height
    total_shape_area = sum(get_shape_area(shapes[sid]) * cnt for sid, cnt in enumerate(counts))
    
    can_fit = total_shape_area <= grid_area
    if can_fit:
        count_area_only += 1
    
    if i < 10:  # Show first 10
        print(f"Region {i+1}: {width}x{height}={grid_area}, needs {total_shape_area}: {'✓' if can_fit else '✗'}")

print(f"\nRegions that pass area test: {count_area_only}")
