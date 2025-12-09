def point_in_polygon(point, polygon):
    """
    Check if a point is inside or on the boundary of a polygon using ray casting.
    """
    x, y = point
    n = len(polygon)
    inside = False
    
    # Check if point is on any edge
    for i in range(n):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % n]
        
        # Check if point is on this edge
        if min(x1, x2) <= x <= max(x1, x2) and min(y1, y2) <= y <= max(y1, y2):
            # Check if point is collinear with the edge
            cross = (y - y1) * (x2 - x1) - (x - x1) * (y2 - y1)
            if cross == 0:
                return True
    
    # Ray casting algorithm for interior points
    p1x, p1y = polygon[0]
    for i in range(1, n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    
    return inside

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

print("Testing example rectangles:")
print("\n1. Rectangle from 9,5 to 2,3 (area 24, should be valid):")
corners = [(2,3), (2,5), (9,3), (9,5)]
all_valid = all(point_in_polygon(c, positions) for c in corners)
print(f"   All corners valid: {all_valid}")
for c in corners:
    print(f"   {c}: {point_in_polygon(c, positions)}")

print("\n2. Rectangle from 7,1 to 11,7 (area 35, might be invalid):")
corners = [(7,1), (7,7), (11,1), (11,7)]
all_valid = all(point_in_polygon(c, positions) for c in corners)
print(f"   All corners valid: {all_valid}")
for c in corners:
    print(f"   {c}: {point_in_polygon(c, positions)}")

# Find all valid rectangles
print("\n\nFinding all valid rectangles:")
n = len(positions)
valid_rectangles = []

for i in range(n):
    for j in range(i + 1, n):
        x1, y1 = positions[i]
        x2, y2 = positions[j]
        
        min_x, max_x = min(x1, x2), max(x1, x2)
        min_y, max_y = min(y1, y2), max(y1, y2)
        
        corners = [(min_x, min_y), (min_x, max_y), (max_x, min_y), (max_x, max_y)]
        
        if all(point_in_polygon(c, positions) for c in corners):
            width = abs(x2 - x1) + 1
            height = abs(y2 - y1) + 1
            area = width * height
            valid_rectangles.append((area, i, j, positions[i], positions[j]))

valid_rectangles.sort(reverse=True)
print(f"Found {len(valid_rectangles)} valid rectangles")
print("Top 10:")
for area, i, j, pos1, pos2 in valid_rectangles[:10]:
    print(f"  Area {area}: positions[{i}]={pos1} to positions[{j}]={pos2}")
