# 2.)
def my_func1(number1, number2, operation):
    match operation:
        case "add":
            return number1 + number2
        case "sub":
            return number1 - number2
        case "mul":
            return number1 * number2
        case "div":
            if number2 is 0:
                return "NaN"
            return number1 / number2

