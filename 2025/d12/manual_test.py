#!/usr/bin/env python3
"""
Minimal test - manually implement for the 4x4 case
"""

# Shape 4: ###
#          #..
#          ###
# That's 7 cells in a 3x3 bounding box

# 4x4 grid, need to place 2 of shape 4

# Let's manually enumerate some placements
# Shape 4 cells (0-indexed): (0,0), (0,1), (0,2), (1,0), (2,0), (2,1), (2,2)

def print_grid(grid):
    for row in grid:
        print(''.join('█' if c else '·' for c in row))
    print()

# Try placing first shape at (0, 0)
grid = [[False]*4 for _ in range(4)]

# First shape at (0,0)
for r, c in [(0,0), (0,1), (0,2), (1,0), (2,0), (2,1), (2,2)]:
    grid[r][c] = True

print("After placing first shape at (0,0):")
print_grid(grid)

# Can we fit second shape?
# Try (1,2):
# Cells would be: (1,2), (1,3), (1,4-out!), ...
# Try (0,3): Can't, (0,3) itself but then (0,4), (0,5) are out
# Try (1,1):
# Cells would be: (1,1), (1,2), (1,3), (2,1-occupied!), ...

# Try (1,2):
coords_shifted = [(r+1, c+2) for r, c in [(0,0), (0,1), (0,2), (1,0), (2,0), (2,1), (2,2)]]
print("Second shape at offset (1,2) would be:", coords_shifted)
valid = all(0 <= r < 4 and 0 <= c < 4 and not grid[r][c] for r, c in coords_shifted)
print("Valid?", valid)

# Let me try a different strategy - place first at different position
grid2 = [[False]*4 for _ in range(4)]

# Shape 4 can also be flipped/rotated. Let me try: rotate 180
# Original: ###    Rotated 180: ###
#           #..                   ..#
#           ###                   ###
rotated = [(2,2), (2,1), (2,0), (1,2), (0,2), (0,1), (0,0)]

for r, c in rotated:
    grid2[r][c] = True
print("First shape rotated 180 at (0,0):")
print_grid(grid2)

# Now try second shape (original orientation) at (1,0)
coords2 = [(r+1, c+0) for r, c in [(0,0), (0,1), (0,2), (1,0), (2,0), (2,1), (2,2)]]
print("Second at (1,0):", coords2)
valid2 = all(0 <= r < 4 and 0 <= c < 4 and not grid2[r][c] for r, c in coords2)
print("Valid?", valid2)

if valid2:
    for r, c in coords2:
        grid2[r][c] = True
    print("Both shapes placed:")
    print_grid(grid2)
