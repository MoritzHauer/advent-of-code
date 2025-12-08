import heapq
from collections import defaultdict


class UnionFind:
    """Union-Find (Disjoint Set Union) data structure."""
    
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
    
    def find(self, x):
        """Find the root of x with path compression."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        """Union the sets containing x and y."""
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return False  # Already in same set
        
        # Union by size
        if self.size[root_x] < self.size[root_y]:
            root_x, root_y = root_y, root_x
        
        self.parent[root_y] = root_x
        self.size[root_x] += self.size[root_y]
        return True
    
    def get_circuit_sizes(self):
        """Get sizes of all circuits."""
        circuits = defaultdict(int)
        for i in range(len(self.parent)):
            root = self.find(i)
            circuits[root] = self.size[root]
        return list(circuits.values())


def parse_input(input_text):
    """Parse junction box positions."""
    positions = []
    for line in input_text.strip().split('\n'):
        x, y, z = map(int, line.split(','))
        positions.append((x, y, z))
    return positions


def distance(p1, p2):
    """Calculate Euclidean distance between two points."""
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 + (p1[2] - p2[2])**2) ** 0.5


def solve(input_text, num_connections=1000, debug=False):
    """
    Connect the closest pairs of junction boxes and find circuit sizes.
    
    Args:
        input_text: Input containing junction box positions
        num_connections: Number of connections to make
        debug: If True, print circuit sizes
    
    Returns:
        Product of the three largest circuit sizes
    """
    positions = parse_input(input_text)
    n = len(positions)
    
    # Create a min-heap of all pairwise distances
    distances = []
    for i in range(n):
        for j in range(i + 1, n):
            dist = distance(positions[i], positions[j])
            heapq.heappush(distances, (dist, i, j))
    
    # Union-Find to track circuits
    uf = UnionFind(n)
    
    # Process the num_connections shortest pairs (whether they connect or not)
    for idx in range(min(num_connections, len(distances))):
        dist, i, j = heapq.heappop(distances)
        uf.union(i, j)  # Doesn't matter if it succeeds or not
    
    # Get circuit sizes and find product of three largest
    circuit_sizes = uf.get_circuit_sizes()
    circuit_sizes.sort(reverse=True)
    
    if debug:
        print(f"Circuit sizes: {circuit_sizes}")
    
    # Multiply the three largest (or however many we have)
    if len(circuit_sizes) >= 3:
        result = circuit_sizes[0] * circuit_sizes[1] * circuit_sizes[2]
    elif len(circuit_sizes) == 2:
        result = circuit_sizes[0] * circuit_sizes[1]
    elif len(circuit_sizes) == 1:
        result = circuit_sizes[0]
    else:
        result = 0
    
    return result


# Test with the example
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

print("Example (10 connections):")
result = solve(example, num_connections=10, debug=True)
print(f"Product of three largest circuits: {result}")
print(f"Expected: 40")
print()

# Solve the actual puzzle
import os
for filename in ['input.txt', 'input']:
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            puzzle_input = f.read()
        print("Puzzle answer (1000 connections):")
        answer = solve(puzzle_input, num_connections=1000)
        print(f"Product of three largest circuits: {answer}")
        break
else:
    print("No input file found.")
