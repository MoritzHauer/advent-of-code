import heapq
import math

example = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689"""

positions = []
for line in example.strip().split('\n'):
    x, y, z = map(int, line.split(','))
    positions.append((x, y, z))

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 + (p1[2] - p2[2])**2)

# Create all pairs with distances
pairs = []
n = len(positions)
for i in range(n):
    for j in range(i + 1, n):
        dist = distance(positions[i], positions[j])
        pairs.append((dist, i, j))

pairs.sort()

# Simulate Union-Find
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return False  # Already connected
        
        # Union by size
        if self.size[root_x] < self.size[root_y]:
            self.parent[root_x] = root_y
            self.size[root_y] += self.size[root_x]
        else:
            self.parent[root_y] = root_x
            self.size[root_x] += self.size[root_y]
        
        return True

uf = UnionFind(n)

# Print first 15 pairs and try connecting them
print("Making connections (first 10 pairs, regardless of success):")
for idx in range(min(10, len(pairs))):
    dist, i, j = pairs[idx]
    if uf.union(i, j):
        print(f"Pair {idx+1}: box {i} <-> box {j} (distance {dist:.2f}) - CONNECTED")
    else:
        print(f"Pair {idx+1}: box {i} <-> box {j} (distance {dist:.2f}) - ALREADY CONNECTED")

# Get circuit sizes
from collections import defaultdict
circuits = defaultdict(list)
for i in range(n):
    root = uf.find(i)
    circuits[root].append(i)

print("\nCircuits:")
circuit_sizes = []
for root, members in circuits.items():
    size = len(members)
    circuit_sizes.append(size)
    print(f"Circuit with {size} boxes: {members}")

circuit_sizes.sort(reverse=True)
print(f"\nCircuit sizes (sorted): {circuit_sizes}")
print(f"Product of three largest: {circuit_sizes[0] * circuit_sizes[1] * circuit_sizes[2]}")
