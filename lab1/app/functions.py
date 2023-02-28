import constants as const


# 2.)
def my_func1(number1, number2, operation):
    match operation:
        case const.SUMMATION:
            return number1 + number2
        case const.SUBTRACTION:
            return number1 - number2
        case const.MULTIPLICATION:
            return number1 * number2
        case const.DIVISION:
            if number2 is 0:
                return "NaN"
            return number1 / number2

