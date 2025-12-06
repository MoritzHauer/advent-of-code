def parse_worksheet(input_text):
    """
    Parse the math worksheet into individual problems.
    
    Each problem's numbers are arranged vertically, with the operation at the bottom.
    Problems are separated by full columns of spaces.
    
    Args:
        input_text: Multi-line string representing the worksheet
    
    Returns:
        List of tuples (numbers_list, operation) for each problem
    """
    lines = input_text.strip().split('\n')
    
    # Determine the width of the worksheet
    max_width = max(len(line) for line in lines)
    
    # Pad all lines to the same width
    padded_lines = [line.ljust(max_width) for line in lines]
    
    # Find problem boundaries (columns that are entirely spaces except for the operator)
    problems = []
    current_problem = []
    
    col = 0
    while col < max_width:
        # Check if this column is the start or part of a problem
        # A column is part of a problem if any non-last row has a non-space character
        is_problem_col = any(padded_lines[row][col] != ' ' for row in range(len(padded_lines)))
        
        if is_problem_col:
            # Start or continue a problem
            current_problem.append(col)
        else:
            # End of a problem (separator column)
            if current_problem:
                # Extract this problem
                problem_numbers = []
                operation = None
                
                for row in range(len(padded_lines) - 1):
                    # Extract number from this row
                    num_str = ''.join(padded_lines[row][c] for c in current_problem).strip()
                    if num_str:
                        problem_numbers.append(int(num_str))
                
                # Get the operation from the last row
                op_str = ''.join(padded_lines[-1][c] for c in current_problem).strip()
                operation = op_str
                
                problems.append((problem_numbers, operation))
                current_problem = []
        
        col += 1
    
    # Handle the last problem if it exists
    if current_problem:
        problem_numbers = []
        operation = None
        
        for row in range(len(padded_lines) - 1):
            num_str = ''.join(padded_lines[row][c] for c in current_problem).strip()
            if num_str:
                problem_numbers.append(int(num_str))
        
        op_str = ''.join(padded_lines[-1][c] for c in current_problem).strip()
        operation = op_str
        
        problems.append((problem_numbers, operation))
    
    return problems


def solve_problem(numbers, operation):
    """
    Solve a single math problem.
    
    Args:
        numbers: List of numbers to combine
        operation: '+' for addition or '*' for multiplication
    
    Returns:
        The result of the operation
    """
    if not numbers:
        return 0
    
    if operation == '+':
        return sum(numbers)
    elif operation == '*':
        result = 1
        for num in numbers:
            result *= num
        return result
    else:
        raise ValueError(f"Unknown operation: {operation}")


def solve(input_text):
    """
    Solve the math worksheet and return the grand total.
    
    Args:
        input_text: Multi-line string representing the worksheet
    
    Returns:
        The grand total (sum of all problem results)
    """
    problems = parse_worksheet(input_text)
    
    grand_total = 0
    for numbers, operation in problems:
        result = solve_problem(numbers, operation)
        grand_total += result
    
    return grand_total


# Test with the example from the puzzle description
example = """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  """

print("Example:")
result = solve(example)
print(f"Grand total: {result}")
print(f"Expected: 4277556")
print()

# Solve the actual puzzle
import os
for filename in ['input.txt', 'input']:
    filepath = os.path.join(os.path.dirname(__file__), filename)
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            puzzle_input = f.read()
        print("Part 1 answer:")
        answer = solve(puzzle_input)
        print(f"Grand total: {answer}")
        break
else:
    print("No input file found.")
