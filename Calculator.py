# Check if the input token is a valid number (integer, decimal, or negative)
def is_number(token):
    try:
        float(token)
        return True
    except ValueError:
        return False


# Convert an infix expression to Reverse Polish Notation (RPN)
# using the Shunting Yard algorithm. This makes evaluation easier by prioritising operator precedence.
def shunting_yard(expression):
    precedence = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3}
    right_associative = ["^"]

    # Split expression into a list of characters
    infix = [char for char in expression]
    previous_token = None
    output_queue = []
    operator_stack = []
    equation = []
    number = ""

    # Combine digits (and decimal points) into multi-digit numbers
    for i, char in enumerate(infix):
        if char.isdigit() or char == ".":
            number += char
        # Handle unary minus (negative numbers)
        elif char == "-" and (i == 0 or previous_token in precedence or previous_token == "("):
            number += char
        # Handle unary plus (rare but valid case, e.g., +5)
        elif char == "+" and (i == 0 or previous_token in precedence or previous_token == "("):
            number += char
        # Handle operators and parentheses
        elif char in precedence or char in "()":
            if number != "":
                equation.append(number)
                number = ""
            equation.append(char)
        else:
            raise ValueError("Invalid character")
        previous_token = char

    if number != "":
        equation.append(number)

    # Convert to RPN
    for token in equation:
        if is_number(token):
            output_queue.append(token)
        elif token in precedence:
            while (operator_stack and operator_stack[-1] in precedence and
                   ((precedence[operator_stack[-1]] > precedence[token]) or
                    (precedence[operator_stack[-1]] == precedence[token] and token not in right_associative))):
                output_queue.append(operator_stack.pop())
            operator_stack.append(token)
        elif token == "(":
            operator_stack.append(token)
        elif token == ")":
            while operator_stack and operator_stack[-1] != "(":
                output_queue.append(operator_stack.pop())
            operator_stack.pop()


    # Pop any remaining operators
    while operator_stack:
        if operator_stack[-1] in "()":
            raise ValueError("Mismatched parentheses")
        output_queue.append(operator_stack.pop())

    return output_queue


# Evaluate an expression in Reverse Polish Notation
def evaluate_rpn(rpn):
    stack = []
    for token in rpn:
        if is_number(token):
            stack.append(float(token))
        else:
            num2 = stack.pop()
            num1 = stack.pop()
            if token == "+":
                stack.append(num1 + num2)
            elif token == "-":
                stack.append(num1 - num2)
            elif token == "*":
                stack.append(num1 * num2)
            elif token == "/":
                if num2 == 0:
                    raise ZeroDivisionError("Division by zero")
                stack.append(num1 / num2)
            elif token == "^":
                stack.append(num1 ** num2)
    return stack[0]


# Main calculator function
def calculator(equation):
    rpn = shunting_yard(equation)
    result = evaluate_rpn(rpn)

    if result.is_integer():
        result = int(result)
    return result


# Command-line loop
while True:
    print("Enter an expression or 'quit' to exit the program")
    user_input = input("Enter an expression: ").replace(" ", "")
    if user_input == "quit":
        print("You have stopped the program!")
        break
    elif user_input == "":
        print("Please enter a valid expression!")
    else:
        try:
            solution = calculator(user_input)
            print(f"Answer: {solution}")
        except Exception as e:
            print(f"Error: {e}")
    print("-" * 30)
