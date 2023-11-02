import sys

variables = {}

def perform_assignment(line):
    items = [item.strip() for item in line.split('=')]
    variable_name = items[0].strip()
    expression = items[1].strip()
    result = evaluate_expression(expression)
    if 'bastir' in expression:
        print_target = extract_value(expression, 'bastir')
        print(print_target)
        user_input = input().strip()
        variables[variable_name] = user_input
    elif result is not None:
        variables[variable_name] = result

def evaluate_expression(expression):
    expression = expression.replace(' ', '')
    result = evaluate_addition_subtraction(expression)
    return result

def evaluate_addition_subtraction(expression):
    terms = split_expression(expression, ['+', '-'])
    result = evaluate_multiplication_division(terms[0])
    i = 1
    while i < len(terms):
        operator = terms[i]
        i += 1
        if operator == '+':
            result += evaluate_multiplication_division(terms[i])
        elif operator == '-':
            result -= evaluate_multiplication_division(terms[i])
        i += 1
    return result

def evaluate_multiplication_division(term):
    factors = split_expression(term, ['*', '/'])
    result = evaluate_factor(factors[0])
    i = 1
    while i < len(factors):
        operator = factors[i]
        i += 1
        if operator == '*':
            result *= evaluate_factor(factors[i])
        elif operator == '/':
            fractional = evaluate_factor(factors[i])
            if fractional == 0:
                print("Sıfıra bölme hatası")
                return None
            result /= fractional
        i += 1
    return result

def evaluate_factor(factor):
    if factor in variables:
        return int(variables[factor])
    try:
        return int(factor)
    except ValueError:
        return None

def execute_print(line):
    print_target = extract_value(line, 'yaz')
    print(print_target)

def extract_value(text, command):
    text_list = text.split(command)
    result = ""
    for item in text_list[1:]:
        value = extract_string_or_variable(item)
        result += str(value)
    return result

def extract_string_or_variable(text):
    if text[0] == '(' and (text[1] == '"' or text[1] == "'"):
        closing_char = text[1]
        value = ""
        index = 2
        while index < len(text):
            if text[index] == closing_char and text[index + 1] == ")":
                break
            value += text[index]
            index += 1
        return value
    elif text[0] == '(':
        index = 1
        variable_name = ""
        while index < len(text):
            if text[index] == ')':
                break
            variable_name += text[index]
            index += 1
        variable_name = variable_name.strip()
        return variables.get(variable_name, '')
    return ""

def find_equality(line):
    if '=' in line:
        perform_assignment(line)
    elif 'yaz' in line:
        execute_print(line)
    else:
        print("Bilinmeyen ifade: ", line)

def get_from_file(file_name):
    with open(file_name) as file_object:
        return file_object.read()

def get_lines(file_name):
    text = get_from_file(file_name)
    lines = text.split("\n")
    for line in lines:
        find_equality(line)


def split_expression(expression, operators):
    current_term = ""
    terms = []
    for char in expression:
        if char in operators:
            terms.append(current_term)
            terms.append(char)
            current_term = ""
        else:
            current_term += char
    terms.append(current_term)
    return terms


if len(sys.argv) < 2:
    get_lines("deneme.txt")
else:
    dosya_adi = sys.argv[1]
    try:
        with open(dosya_adi, "r") as file:
            text = file.read()
            lines = text.split("\n")
            for line in lines:
                find_equality(line)
    except FileNotFoundError:
        print(f"{dosya_adi} adlı dosya bulunamadı.")
