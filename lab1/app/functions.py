import constants as const


# 2.)
def my_func1(number1, number2, operation):

    if type(number1) is not int and type(number1) is not float:
        return "NaN"
    if type(number2) is not int and type(number2) is not float:
        return "NaN"

    match operation:
        case const.SUMMATION:
            return number1 + number2
        case const.SUBTRACTION:
            return number1 - number2
        case const.MULTIPLICATION:
            return number1 * number2
        case const.DIVISION:
            if number2 == 0:
                return "NaN"
            return number1 / number2


# 3.)
def my_func2(list1):
    return [number for number in list1 if not number % 2]

