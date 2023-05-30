from sys import argv
import re
import datetime
from random import randint


def push(obj, l, depth):
    while depth:
        l = l[-1]
        depth -= 1

    l.append(obj)

def parse_parentheses(s):
    groups = []
    depth = 0

    try:
        for char in s:
            if char == '(':
                push([], groups, depth)
                depth += 1
            elif char == ')':
                depth -= 1
            else:
                push(char, groups, depth)
    except IndexError:
        raise ValueError('Parentheses mismatch')

    if depth > 0:
        raise ValueError('Parentheses mismatch')
    else:
        return groups

    
def get_paren(expr):
    return parse_parentheses(expr)
    
def add(vals):
    vals = vals.split("+")
    total = int(vals[0])
    vals.pop(0)
    for val in vals:
        total += int(val)
    return total

def sub(vals):
    vals = vals.split("-")
    total = int(vals[0])
    vals.pop(0)
    for val in vals:
        total -= int(val)
    return total

def mul(vals):
    vals = vals.split("*")
    total = int(vals[0])
    vals.pop(0)
    for val in vals:
        total *= int(val)
    return total

def div(vals):
    vals = vals.split("/")
    total = float(vals[0])
    vals.pop(0)
    for val in vals:
        total /= float(val)
    return total

def contains_op(expr):
    return re.search("[+-/\*]", expr) != None

def get_op(expr):
    return re.search("[+-/\*]", expr).group(0)

def contains_nested(paren):
    try:
        return any(isinstance(p, list) for p in paren)
    except TypeError:
        return False

def simplify(parens, updated):
    #print(f"Simplify: Parens: {parens}, Updated: {updated}")
    if(len(parens) == 0):
        return updated
    expr = parens[0]
    if type(expr) == str and expr in "+-/*":
        updated.append(expr)
        return simplify(parens[1:], updated)
    if type(expr) == str and expr not in "+-/*" and updated[-1] not in "+-/*":
        updated[-1] += expr
        return simplify(parens[1:], updated)
    if type(expr) == str and expr not in "+-/*":
        updated.append(expr)
        return simplify(parens[1:], updated)
    if contains_nested(expr):
        return simplify(parens[0], updated)
        updated.append(expr)
    expr = "".join(expr)
    if contains_op(expr):
        op = get_op(expr)
        if op == "*":
            updated.append(str(mul(expr)))
        elif op == "/":
            updated.append(str(div(expr)))
        elif op == "+":
            updated.append(str(add(expr)))
            # print(updated)
        elif op == "-":
            updated.append(str(sub(expr)))
        
    return simplify(parens[1:], updated)

def calculate_left_right(parsed, op_index, action):
    left = float(parsed[op_index - 1])
    right = float(parsed[op_index + 1])
    parsed.pop(op_index - 1)
    parsed.pop(op_index - 1)
    if action == "*":
        parsed[op_index - 1] = str(left * right)
    elif action == "/":
        parsed[op_index - 1] = str(left / right)
    elif action == "+":
        parsed[op_index - 1] = str(left + right)
    elif action == "-":
        parsed[op_index - 1] = str(left - right)
    return parsed

    

def calc(parsed):
    #print(f"Calc: Parsed = {parsed}")
    if len(parsed) == 1:
        return parsed
    divi = -1
    mult = -1
    # calc pemdas
    if "/" in parsed:
        divi = parsed.index("/")
    if "*" in parsed:
        mult = parsed.index("*")
    if divi > -1 and mult > -1:
        if mult < divi: # multiply first
            calculate_left_right(parsed, mult, "*")
            # do divide next
            divi = parsed.index("/") # Find new divide sign
            calculate_left_right(parsed, divi, "/")
        elif divi < mult:
            calculate_left_right(parsed, divi, "/")
            mult = parsed.index("*")
            calculate_left_right(parsed, mult, "*")
    elif mult > -1 and divi == -1:
        calculate_left_right(parsed, mult, "*")
        
    elif divi > -1 and mult == -1:
        calculate_left_right(parsed, divi, "/")        
    else:
        add = -1
        sub = -1
        if "+" in parsed:
            add = parsed.index("+")
        if "-" in parsed:
            sub = parsed.index("-")
        if add > -1 and sub > -1:
            if add < sub:
                calculate_left_right(parsed, add, "+")
                sub = parsed.index("-")
                calculate_left_right(parsed, sub, "-")
            elif add > sub:
                calculate_left_right(parsed, sub, "-")
                add = parsed.index("+")
                calculate_left_right(parsed,add, "+")
        elif add > -1 and sub == -1:
            calculate_left_right(parsed, add, "+")
        elif sub > -1 and add == -1:
            calculate_left_right(parsed, sub, "-")    
    return calc(parsed)
    

def parse(expr):
    expr = f"({expr})"
    exprs = []
    expr = expr.replace(" ", "")
    parens = get_paren(expr)
    updated = []
    simplified = simplify(parens, updated)
    calculated = calc(simplified)
    return calculated[0]

def get_digits(expr):
    nums = []
    expr = expr.replace(" ", "")
    temp_num = ""
    for char in expr:
        if char.isdigit():
            temp_num += char
        else:
            nums.append(temp_num)
            temp_num = ""
    nums.append(temp_num)
    pure_nums = []
    for num in nums:
        if num != "":
            pure_nums.append(int(num))
    return nums

def gen_nums():
    nums = []
    for _ in range(3):
        nums.append(randint(1, 21))
        nums.append(randint(1,10))
    nums.pop()
    return nums

def get_date():
    return datetime.datetime.now().day
    
            
if __name__ == "__main__":
    date = float(get_date())
    nums = gen_nums()
    print(f"Number to calculate: {date}")
    print("Nums: ", end="")
    for num in nums:
        print(num, end=" ")
    print()
    guess = -1
    calculation = input("Enter your calculation: ")

    digits = get_digits(calculation)
    
    guess = parse(calculation)
 
    if float(guess) == float(date):
        print("You got it!")
    else:
        print(f"Good try. Your calculation was: {guess}")
