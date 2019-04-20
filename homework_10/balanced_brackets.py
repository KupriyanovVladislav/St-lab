def check_balance_brackets(expr: str) -> bool:
    brackets_dict = {
        ')': '(',
        ']': '[',
        '}': '{',
    }

    stack = []
    opened_brackets = brackets_dict.values()
    closed_brackets = brackets_dict.keys()

    for symbol in expr:

        if symbol in opened_brackets:
            stack.append(symbol)

        elif symbol in closed_brackets:
            if not stack:
                break
            elif stack.pop() != brackets_dict.get(symbol):
                break

    else:
        if not stack:
            return True

    return False
