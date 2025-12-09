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


def solve(input_text, part2=False):
    """
    Count how many of the available ingredient IDs are fresh (part 1),
    or count total fresh IDs in all ranges (part 2).
    
    Args:
        input_text: The database file content
        part2: If True, solve part 2; otherwise solve part 1
    
    Returns:
        Number of fresh ingredients (part 1) or total fresh IDs (part 2)
    """
    ranges, ingredient_ids = parse_input(input_text)
    
    if not part2:
        # Part 1: Count how many available ingredients are fresh
        fresh_count = 0
        for ingredient_id in ingredient_ids:
            if is_fresh(ingredient_id, ranges):
                fresh_count += 1
        return fresh_count
    else:
        # Part 2: Count total unique IDs covered by all ranges
        # Merge overlapping ranges and count total IDs
        if not ranges:
            return 0
        
        # Sort ranges by start position
        sorted_ranges = sorted(ranges)
        
        # Merge overlapping ranges
        merged = [sorted_ranges[0]]
        for start, end in sorted_ranges[1:]:
            last_start, last_end = merged[-1]
            
            # If current range overlaps or is adjacent to last merged range
            if start <= last_end + 1:
                # Merge by extending the end if needed
                merged[-1] = (last_start, max(last_end, end))
            else:
                # No overlap, add as new range
                merged.append((start, end))
        
        # Count total IDs in merged ranges
        total = 0
        for start, end in merged:
            total += end - start + 1
        
        return total


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

print("Part 2 Example:")
result2 = solve(example, part2=True)
print(f"Total fresh IDs in ranges: {result2}")
print(f"Expected: 14")
print()

# Solve the actual puzzle
import os
for filename in ['input.txt', 'input']:
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            puzzle_input = f.read()
        print("Part 1 Puzzle answer:")
        answer1 = solve(puzzle_input)
        print(f"Number of fresh ingredients: {answer1}")
        print()
        print("Part 2 Puzzle answer:")
        answer2 = solve(puzzle_input, part2=True)
        print(f"Total fresh IDs in ranges: {answer2}")
        break
else:
    print("No input file found.")
