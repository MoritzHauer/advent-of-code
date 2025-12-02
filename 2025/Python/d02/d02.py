def is_invalid_id(num, part2=False):
    """
    Check if a number is invalid.
    Part 1: made of a sequence repeated exactly twice (e.g., 11, 6464, 123123)
    Part 2: made of a sequence repeated at least twice (e.g., 111, 12341234, 123123123)
    """
    s = str(num)
    length = len(s)
    
    if not part2:
        # Part 1: Must have even length to be split in half
        if length % 2 != 0:
            return False
        
        # Split in half and check if both halves are identical
        mid = length // 2
        first_half = s[:mid]
        second_half = s[mid:]
        
        return first_half == second_half
    else:
        # Part 2: Check if the string can be formed by repeating a pattern at least twice
        # Try all possible pattern lengths from 1 to length//2
        for pattern_len in range(1, length // 2 + 1):
            # Check if length is divisible by pattern_len
            if length % pattern_len == 0:
                pattern = s[:pattern_len]
                # Check if repeating this pattern gives us the full string
                if pattern * (length // pattern_len) == s:
                    return True
        return False


def find_invalid_ids_in_range(start, end, part2=False):
    """
    Find all invalid IDs in the range [start, end].
    Returns a list of invalid IDs.
    """
    invalid_ids = []
    
    for num in range(start, end + 1):
        if is_invalid_id(num, part2):
            invalid_ids.append(num)
    
    return invalid_ids


def solve(ranges_str, part2=False):
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
        invalid_ids = find_invalid_ids_in_range(start, end, part2)
        all_invalid_ids.extend(invalid_ids)
    
    return sum(all_invalid_ids)


# Test with the example
example = """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124"""

print("Part 1 Example:")
result = solve(example)
print(f"Sum of invalid IDs: {result}")
print(f"Expected: 1227775554")
print()

print("Part 2 Example:")
result2 = solve(example, part2=True)
print(f"Sum of invalid IDs: {result2}")
print(f"Expected: 4174379265")
print()

# Solve the actual puzzle
import os
for filename in ['input.txt', 'input']:
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            puzzle_input = f.read()
        print("Part 1 answer:")
        answer1 = solve(puzzle_input)
        print(f"Sum of invalid IDs: {answer1}")
        print()
        print("Part 2 answer:")
        answer2 = solve(puzzle_input, part2=True)
        print(f"Sum of invalid IDs: {answer2}")
        break
else:
    print("No input file found.")
