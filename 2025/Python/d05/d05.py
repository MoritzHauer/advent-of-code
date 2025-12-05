def parse_input(input_text):
    """
    Parse the database file into ranges and ingredient IDs.
    
    Args:
        input_text: The raw input text
    
    Returns:
        Tuple of (ranges, ingredient_ids)
        - ranges: List of (start, end) tuples
        - ingredient_ids: List of ingredient IDs to check
    """
    parts = input_text.strip().split('\n\n')
    
    # Parse ranges
    ranges = []
    for line in parts[0].split('\n'):
        start, end = map(int, line.split('-'))
        ranges.append((start, end))
    
    # Parse ingredient IDs
    ingredient_ids = [int(line) for line in parts[1].split('\n')]
    
    return ranges, ingredient_ids


def is_fresh(ingredient_id, ranges):
    """
    Check if an ingredient ID is fresh (falls within any range).
    
    Args:
        ingredient_id: The ID to check
        ranges: List of (start, end) tuples representing fresh ranges
    
    Returns:
        True if the ingredient is fresh, False otherwise
    """
    for start, end in ranges:
        if start <= ingredient_id <= end:
            return True
    return False


def solve(input_text):
    """
    Count how many of the available ingredient IDs are fresh.
    
    Args:
        input_text: The database file content
    
    Returns:
        Number of fresh ingredients
    """
    ranges, ingredient_ids = parse_input(input_text)
    
    fresh_count = 0
    for ingredient_id in ingredient_ids:
        if is_fresh(ingredient_id, ranges):
            fresh_count += 1
    
    return fresh_count


# Test with the example
example = """3-5
10-14
16-20
12-18

1
5
8
11
17
32"""

print("Example:")
ranges, ids = parse_input(example)
print(f"Ranges: {ranges}")
print(f"Ingredient IDs: {ids}")
print()

for id_val in ids:
    fresh = is_fresh(id_val, ranges)
    print(f"Ingredient ID {id_val}: {'fresh' if fresh else 'spoiled'}")
print()

result = solve(example)
print(f"Total fresh ingredients: {result}")
print(f"Expected: 3")
print()

# Solve the actual puzzle
import os
for filename in ['input.txt', 'input']:
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            puzzle_input = f.read()
        print("Puzzle answer:")
        answer = solve(puzzle_input)
        print(f"Number of fresh ingredients: {answer}")
        break
else:
    print("No input file found.")
