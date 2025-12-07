import os


def extract_problem(padded_lines, column_indices, cephalopod_mode=False):
    """
    Extract a problem from the padded lines given column indices.
    
    Args:
        padded_lines: List of strings padded to the same width
        column_indices: List of column indices that form this problem
        cephalopod_mode: If True, read numbers in cephalopod format (each column is a digit)
    
    Returns:
        Tuple of (numbers_list, operation)
    """
    if not cephalopod_mode:
        # Part 1: Each row is a complete number
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
    else:
        # Part 2: Each column is a digit, read top-to-bottom to form numbers
        problem_numbers = []
        
        for col in column_indices:
            # Read down this column to form a number
            num_str = ''
            for row in range(len(padded_lines) - 1):
                digit = padded_lines[row][col]
                if digit != ' ':
                    num_str += digit
            if num_str:
                problem_numbers.append(int(num_str))
        
        # Get the operation from the last row (should be same for all columns in problem)
        op_str = padded_lines[-1][column_indices[0]].strip()
        operation = op_str
        
        return (problem_numbers, operation)


def parse_worksheet(input_text, cephalopod_mode=False):
    """
    Parse the math worksheet into individual problems.
    
    Each problem's numbers are arranged vertically, with the operation at the bottom.
    Problems are separated by full columns of spaces.
    
    Args:
        input_text: Multi-line string representing the worksheet
        cephalopod_mode: If True, parse in cephalopod format (right-to-left, each column is a digit)
    
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
    
    # In cephalopod mode, read right-to-left
    col_range = range(max_width - 1, -1, -1) if cephalopod_mode else range(max_width)
    
    for col in col_range:
        # Check if this column is the start or part of a problem
        # A column is part of a problem if any non-last row has a non-space character
        is_problem_col = any(padded_lines[row][col] != ' ' for row in range(len(padded_lines)))
        
        if is_problem_col:
            # Start or continue a problem
            if cephalopod_mode:
                current_problem.insert(0, col)  # Insert at beginning to maintain correct order
            else:
                current_problem.append(col)
        else:
            # End of a problem (separator column)
            if current_problem:
                problems.append(extract_problem(padded_lines, current_problem, cephalopod_mode))
                current_problem = []
    
    # Handle the last problem if it exists
    if current_problem:
        problems.append(extract_problem(padded_lines, current_problem, cephalopod_mode))
    
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


def solve(input_text, cephalopod_mode=False):
    """
    Solve the math worksheet and return the grand total.
    
    Args:
        input_text: Multi-line string representing the worksheet
        cephalopod_mode: If True, parse in cephalopod format (right-to-left, each column is a digit)
    
    Returns:
        The grand total (sum of all problem results)
    """
    problems = parse_worksheet(input_text, cephalopod_mode)
    
    grand_total = 0
    for numbers, operation in problems:
        result = solve_problem(numbers, operation)
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

    print("Example Part 2 (cephalopod mode):")
    result_part2 = solve(example, cephalopod_mode=True)
    print(f"Grand total: {result_part2}")
    print(f"Expected: 3263827")
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
            answer_part2 = solve(puzzle_input, cephalopod_mode=True)
            print(f"Grand total: {answer_part2}")
            break
    else:
        print("No input file found.")
