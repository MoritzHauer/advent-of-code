#!/usr/bin/env python3
"""
Day 11: Reactor - Find all paths from 'you' to 'out'

This is a graph path enumeration problem. We need to:
1. Parse the input to build a directed graph
2. Use DFS to find all paths from 'you' to 'out'
3. Count the total number of paths
"""

from typing import Dict, List, Set


def parse_input(filename: str) -> Dict[str, List[str]]:
    """Parse the input file and build the adjacency list graph."""
    graph = {}
    
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            # Parse "device: output1 output2 ..."
            parts = line.split(': ')
            device = parts[0]
            outputs = parts[1].split() if len(parts) > 1 else []
            
            graph[device] = outputs
    
    return graph


def count_paths(graph: Dict[str, List[str]], start: str, end: str) -> int:
    """
    Count all paths from start to end using DFS.
    
    We use backtracking to explore all possible paths:
    - Track visited nodes in current path to avoid cycles
    - When we reach the end, increment count
    - Backtrack to explore other paths
    """
    def dfs(current: str, visited: Set[str]) -> int:
        # Base case: reached the destination
        if current == end:
            return 1
        
        # Dead end: no outgoing connections
        if current not in graph:
            return 0
        
        # Explore all neighbors
        total_paths = 0
        for neighbor in graph[current]:
            # Avoid cycles - don't revisit nodes in current path
            if neighbor not in visited:
                visited.add(neighbor)
                total_paths += dfs(neighbor, visited)
                visited.remove(neighbor)  # Backtrack
        
        return total_paths
    
    # Start DFS with initial node in visited set
    return dfs(start, {start})


def solve_part1(filename: str) -> int:
    """Solve part 1 - count paths from 'you' to 'out'."""
    graph = parse_input(filename)
    return count_paths(graph, 'you', 'out')


# Test with example
example_input = """aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out"""

# Create example file
with open('example', 'w') as f:
    f.write(example_input)

# Test example
print("=== Part 1 ===")
example_result = solve_part1('example')
print(f"Example: {example_result} paths (expected 5)")

# Solve actual puzzle
result = solve_part1('input')
print(f"Part 1 answer: {result}")
