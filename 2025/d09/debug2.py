example = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""

positions = []
for line in example.strip().split('\n'):
    x, y = map(int, line.split(','))
    positions.append((x, y))

print("Red tile positions (in order):")
for i, pos in enumerate(positions):
    print(f"{i}: {pos}")

print("\nChecking the example rectangles:")
print("\n1. Rectangle from 9,5 to 2,3 (expected area 24):")
x1, y1 = 2, 3
x2, y2 = 9, 5
width = abs(x2 - x1) + 1
height = abs(y2 - y1) + 1
print(f"   Corners: ({x1},{y1}) to ({x2},{y2})")
print(f"   Width: {width}, Height: {height}, Area: {width * height}")
print(f"   All corners: ({x1},{y1}), ({x1},{y2}), ({x2},{y1}), ({x2},{y2})")

print("\n2. Rectangle from 9,7 to 9,5 (expected area 3):")
x1, y1 = 9, 5
x2, y2 = 9, 7
width = abs(x2 - x1) + 1
height = abs(y2 - y1) + 1
print(f"   Corners: ({x1},{y1}) to ({x2},{y2})")
print(f"   Width: {width}, Height: {height}, Area: {width * height}")

print("\n3. Rectangle from 7,3 to 11,1 (expected area 15):")
x1, y1 = 7, 3
x2, y2 = 11, 1
width = abs(x2 - x1) + 1
height = abs(y2 - y1) + 1
print(f"   Corners: ({x1},{y1}) to ({x2},{y2})")
print(f"   Width: {width}, Height: {height}, Area: {width * height}")
