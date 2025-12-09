def find_max_joltage(bank, num_batteries=2):
    """
    Find the maximum joltage possible from a bank by selecting
    exactly num_batteries batteries (maintaining their order).
    
    Strategy: Greedily select batteries to maximize the resulting number.
    At each position, choose to keep or skip the battery.
    
    Args:
        bank: A string of digits representing battery joltages
        num_batteries: Number of batteries to select
    
    Returns:
        The maximum joltage possible
    """
    if num_batteries == 2:
        # Optimized approach for 2 batteries
        n = len(bank)
        max_joltage = 0
        
        for i in range(n - 1):
            max_after = max(bank[i + 1:])
            joltage = int(bank[i] + max_after)
            max_joltage = max(max_joltage, joltage)
        
        return max_joltage
    
    # For selecting k batteries from n positions to maximize the number
    # We use a greedy approach: at each step, choose the largest digit
    # that still allows us to select enough remaining batteries
    n = len(bank)
    k = num_batteries
    result = []
    start = 0
    
    for i in range(k):
        # We need to select k-i batteries starting from position start
        # We must leave at least k-i-1 positions after our choice
        best_digit = '0'
        best_pos = start
        
        # We can choose from positions start to n-(k-i)
        for pos in range(start, n - (k - i) + 1):
            if bank[pos] > best_digit:
                best_digit = bank[pos]
                best_pos = pos
        
        result.append(best_digit)
        start = best_pos + 1
    
    return int(''.join(result))


def solve(input_text, num_batteries=2):
    """
    Calculate the total output joltage from all battery banks.
    
    Args:
        input_text: Multi-line string where each line is a battery bank
        num_batteries: Number of batteries to select from each bank
    
    Returns:
        The sum of maximum joltages from all banks
    """
    lines = input_text.strip().split('\n')
    total = 0
    
    for bank in lines:
        max_joltage = find_max_joltage(bank, num_batteries)
        total += max_joltage
    
    return total


# Test with the example
example = """987654321111111
811111111111119
234234234234278
818181911112111"""

print("Part 1 Example:")
print("Bank 987654321111111 -> max joltage:", find_max_joltage("987654321111111", 2))
print("Bank 811111111111119 -> max joltage:", find_max_joltage("811111111111119", 2))
print("Bank 234234234234278 -> max joltage:", find_max_joltage("234234234234278", 2))
print("Bank 818181911112111 -> max joltage:", find_max_joltage("818181911112111", 2))
print()

result = solve(example, 2)
print(f"Total output joltage: {result}")
print(f"Expected: 357")
print()

print("Part 2 Example:")
print("Bank 987654321111111 -> max joltage:", find_max_joltage("987654321111111", 12))
print("Bank 811111111111119 -> max joltage:", find_max_joltage("811111111111119", 12))
print("Bank 234234234234278 -> max joltage:", find_max_joltage("234234234234278", 12))
print("Bank 818181911112111 -> max joltage:", find_max_joltage("818181911112111", 12))
print()

result2 = solve(example, 12)
print(f"Total output joltage: {result2}")
print(f"Expected: 3121910778619")
print()

# Solve the actual puzzle
import os
for filename in ['input.txt', 'input']:
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            puzzle_input = f.read()
        print("Part 1 Puzzle answer:")
        answer1 = solve(puzzle_input, 2)
        print(f"Total output joltage: {answer1}")
        print()
        print("Part 2 Puzzle answer:")
        answer2 = solve(puzzle_input, 12)
        print(f"Total output joltage: {answer2}")
        break
else:
    print("No input file found.")
