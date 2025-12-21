#!/usr/bin/env python3
"""Decode the example solution"""

# Example solution:
# AAA.
# ABAB
# ABAB
# .BBB

grid = [
    ['A', 'A', 'A', '.'],
    ['A', 'B', 'A', 'B'],
    ['A', 'B', 'A', 'B'],
    ['.', 'B', 'B', 'B']
]

A_cells = []
B_cells = []

for r in range(4):
    for c in range(4):
        if grid[r][c] == 'A':
            A_cells.append((r, c))
        elif grid[r][c] == 'B':
            B_cells.append((r, c))

print("A cells:", sorted(A_cells))
print("B cells:", sorted(B_cells))
print(f"A has {len(A_cells)} cells")
print(f"B has {len(B_cells)} cells")

# Shape 4: ###
#          #..
#          ###
shape4_cells = [(0,0), (0,1), (0,2), (1,0), (2,0), (2,1), (2,2)]
print(f"\nShape 4 has {len(shape4_cells)} cells: {sorted(shape4_cells)}")

# Normalize A cells
A_min_r = min(r for r,c in A_cells)
A_min_c = min(c for r,c in A_cells)
A_norm = sorted((r-A_min_r, c-A_min_c) for r,c in A_cells)
print(f"\nA normalized: {A_norm}")

B_min_r = min(r for r,c in B_cells)
B_min_c = min(c for r,c in B_cells)
B_norm = sorted((r-B_min_r, c-B_min_c) for r,c in B_cells)
print(f"B normalized: {B_norm}")
print(f"Shape 4: {sorted(shape4_cells)}")
