#!/usr/bin/env python3
"""Test the example from the problem"""

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

with open('test_example', 'w') as f:
    f.write(example_input)

from simple_test import parse_input, get_shape_area

shapes, regions = parse_input('test_example')

print("Shapes:")
for sid in sorted(shapes.keys()):
    print(f"Shape {sid}: {get_shape_area(shapes[sid])} cells")

print("\nRegions:")
for i, (width, height, counts) in enumerate(regions):
    grid_area = width * height
    total_shape_area = sum(get_shape_area(shapes[sid]) * cnt for sid, cnt in enumerate(counts))
    can_fit = total_shape_area <= grid_area
    print(f"Region {i+1}: {width}x{height}={grid_area}, presents={counts}, needs {total_shape_area}: {'✓' if can_fit else '✗'}")

print("\nExpected: 2 regions can fit")
print("Area test gives:", sum(1 for w, h, counts in regions if w*h >= sum(get_shape_area(shapes[sid])*cnt for sid,cnt in enumerate(counts))))
