def is_invalid_id(num):
    """
    Check if a number is invalid (made of a sequence repeated twice).
    Examples: 11 (1 twice), 6464 (64 twice), 123123 (123 twice)
    """
    s = str(num)
    length = len(s)
    
    # Must have even length to be split in half
    if length % 2 != 0:
        return False
    
    # Split in half and check if both halves are identical
    mid = length // 2
    first_half = s[:mid]
    second_half = s[mid:]
    
    return first_half == second_half


def find_invalid_ids_in_range(start, end):
    """
    Find all invalid IDs in the range [start, end].
    Returns a list of invalid IDs.
    """
    invalid_ids = []
    
    for num in range(start, end + 1):
        if is_invalid_id(num):
            invalid_ids.append(num)
    
    return invalid_ids


def solve(ranges_str):
    """
    Parse the input ranges and find all invalid IDs.
    Returns the sum of all invalid IDs.
    """
    # Parse the ranges
    ranges = []
    for range_str in ranges_str.strip().split(','):
        start, end = map(int, range_str.split('-'))
        ranges.append((start, end))
    
    # Find all invalid IDs across all ranges
    all_invalid_ids = []
    for start, end in ranges:
        invalid_ids = find_invalid_ids_in_range(start, end)
        all_invalid_ids.extend(invalid_ids)
    
    return sum(all_invalid_ids)


# Test with the example
example = """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124"""

print("Example:")
result = solve(example)
print(f"Sum of invalid IDs: {result}")
print(f"Expected: 1227775554")
print()

# Solve the actual puzzle
import os
for filename in ['input.txt', 'input']:
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            puzzle_input = f.read()
        print("Puzzle answer:")
        answer = solve(puzzle_input)
        print(f"Sum of invalid IDs: {answer}")
        break
else:
    print("No input file found.")
