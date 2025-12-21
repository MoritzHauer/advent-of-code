#!/usr/bin/env python3
from d12 import *

# Test small example only - First region from the example
example_input = '''4:
###
#..
###

4x4: 0 0 0 0 2 0'''

with open('test_small', 'w') as f:
    f.write(example_input)

shapes, regions = parse_input('test_small')

print("Shapes:")
for sid in shapes:
    print(f"  Shape {sid}:")
    for row in shapes[sid]:
        print(f"    {''.join(row)}")
    coords = get_shape_coords(shapes[sid])
    print(f"    Coords: {coords}")
    print(f"    All orientations: {len(get_all_orientations(shapes[sid]))}")

print("\nRegions:")
for width, height, counts in regions:
    print(f"  {width}x{height}: {counts}")
    result = solve_region(shapes, width, height, counts)
    print(f"  Result: {result}")
