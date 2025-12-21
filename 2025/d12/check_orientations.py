#!/usr/bin/env python3
"""Check if A and B are orientations of shape 4"""

from d12 import get_all_orientations

# Shape 4: ###
#          #..
#          ###
shape4 = [
    ['#', '#', '#'],
    ['#', '.', '.'],
    ['#', '#', '#']
]

orientations = get_all_orientations(shape4)
print(f"Shape 4 has {len(orientations)} unique orientations")

for i, ori in enumerate(orientations):
    print(f"\nOrientation {i}: {sorted(ori)}")

# From the example:
A_norm = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 2)]
B_norm = [(0, 0), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)]

print(f"\nA normalized: {sorted(A_norm)}")
print(f"B normalized: {sorted(B_norm)}")

# Check if either matches
A_matches = [i for i, ori in enumerate(orientations) if set(ori) == set(A_norm)]
B_matches = [i for i, ori in enumerate(orientations) if set(ori) == set(B_norm)]

print(f"\nA matches orientations: {A_matches}")
print(f"B matches orientations: {B_matches}")
