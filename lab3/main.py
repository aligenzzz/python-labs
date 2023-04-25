from json_serializer import JsonSerializer
import types

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

if __name__ == '__main__':
    a = [6, 9, "7658675", {89: 89, 69: 89}]
    b = (5, "jfkg")
    c = True
    d = "abc"
    g = {1, 3, 6, 3}

    json_serializer = JsonSerializer()
    print(json_serializer.dumps(a))
    print(json_serializer.dumps(b))
    print(json_serializer.dumps(c))
    print(json_serializer.dumps(d))
    # print(json_serializer.dumps(g))

    # print(dumps(json_serializer))

    s = {4,4,4}
    print(json_serializer.dumps(s))
    z = 5 + 9j
    print(json_serializer.dumps(z))
    print(json_serializer.dumps(g))

    def parse_function(func):
        fdict = {
            "name": func.__name__,
            "code": func.__code__,
            "globals": func.__globals__,
            "defaults": func.__defaults__,
            "closure": func.__closure__
        }

        return fdict


    def build_function(data):
        return types.FunctionType(data["code"], data["globals"], data["name"], data["defaults"], data["closure"])


    def my_func(x):
        return x ** 2


    parsed_code = parse_function(my_func)
    print(parsed_code)
    new_func = build_function(parsed_code)

    print(new_func(5))

    person = Person("jdfjd", 56)
    print(vars(person))






