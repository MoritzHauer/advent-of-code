def find_max_joltage(bank):
    """
    Find the maximum joltage possible from a bank by selecting
    exactly two batteries (maintaining their order).
    
    Optimized approach: For each digit, track the max digit that comes after it.
    
    Args:
        bank: A string of digits representing battery joltages
    
    Returns:
        The maximum joltage (two-digit number) possible
    """
    n = len(bank)
    max_joltage = 0
    
    # For each position, we only need to know the max digit after it
    for i in range(n - 1):
        # Find max digit from position i+1 to end
        max_after = max(bank[i + 1:])
        joltage = int(bank[i] + max_after)
        max_joltage = max(max_joltage, joltage)
    
    return max_joltage


def solve(input_text):
    """
    Calculate the total output joltage from all battery banks.
    
    Args:
        input_text: Multi-line string where each line is a battery bank
    
    Returns:
        The sum of maximum joltages from all banks
    """
    lines = input_text.strip().split('\n')
    total = 0
    
    for bank in lines:
        max_joltage = find_max_joltage(bank)
        total += max_joltage
    
    return total


# Test with the example
example = """987654321111111
811111111111119
234234234234278
818181911112111"""

print("Example:")
print("Bank 987654321111111 -> max joltage:", find_max_joltage("987654321111111"))
print("Bank 811111111111119 -> max joltage:", find_max_joltage("811111111111119"))
print("Bank 234234234234278 -> max joltage:", find_max_joltage("234234234234278"))
print("Bank 818181911112111 -> max joltage:", find_max_joltage("818181911112111"))
print()

result = solve(example)
print(f"Total output joltage: {result}")
print(f"Expected: 357")
print()

# Solve the actual puzzle
import os
for filename in ['input.txt', 'input']:
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            puzzle_input = f.read()
        print("Puzzle answer:")
        answer = solve(puzzle_input)
        print(f"Total output joltage: {answer}")
        break
else:
    print("No input file found.")
