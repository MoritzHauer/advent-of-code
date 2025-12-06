import os


def extract_problem(padded_lines, column_indices):
    """
    Extract a problem from the padded lines given column indices.
    
    Args:
        padded_lines: List of strings padded to the same width
        column_indices: List of column indices that form this problem
    
    Returns:
        Tuple of (numbers_list, operation)
    """
    problem_numbers = []
    
    for row in range(len(padded_lines) - 1):
        # Extract number from this row
        num_str = ''.join(padded_lines[row][c] for c in column_indices).strip()
        if num_str:
            problem_numbers.append(int(num_str))
    
    # Get the operation from the last row
    op_str = ''.join(padded_lines[-1][c] for c in column_indices).strip()
    operation = op_str
    
    return (problem_numbers, operation)


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
                problems.append(extract_problem(padded_lines, current_problem))
                current_problem = []
        
        col += 1
    
    # Handle the last problem if it exists
    if current_problem:
        problems.append(extract_problem(padded_lines, current_problem))
    
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


def solve(input_text, reverse_numbers=False):
    """
    Solve the math worksheet and return the grand total.
    
    Args:
        input_text: Multi-line string representing the worksheet
        reverse_numbers: If True, reverse the order of numbers in each problem (for Part 2)
    
    Returns:
        The grand total (sum of all problem results)
    """
    problems = parse_worksheet(input_text)
    
    grand_total = 0
    for numbers, operation in problems:
        processed_numbers = numbers[::-1] if reverse_numbers else numbers
        result = solve_problem(processed_numbers, operation)
        grand_total += result
    
    return grand_total


if __name__ == '__main__':
    # Test with the example from the puzzle description
    example = """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  """

    print("Example Part 1:")
    result = solve(example)
    print(f"Grand total: {result}")
    print(f"Expected: 4277556")
    print()

    print("Example Part 2 (reversed):")
    result_part2 = solve(example, reverse_numbers=True)
    print(f"Grand total: {result_part2}")
    print()

    # Solve the actual puzzle
    for filename in ['input.txt', 'input']:
        filepath = os.path.join(os.path.dirname(__file__), filename)
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                puzzle_input = f.read()
            print("Part 1 answer:")
            answer = solve(puzzle_input)
            print(f"Grand total: {answer}")
            print()
            print("Part 2 answer:")
            answer_part2 = solve(puzzle_input, reverse_numbers=True)
            print(f"Grand total: {answer_part2}")
            break
    else:
        print("No input file found.")
