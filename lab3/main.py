import sys

from json_serializer import JsonSerializer

import math

A = 6

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @staticmethod
    def koko(x):
        return x * 2

if __name__ == '__main__':
    a = [6, 9, "7658675", {89: 89, 69: 89}, [1, 2, 3]]
    b = (5, "pam")
    c = True
    d = "abc"
    g = {1, 3, 6, 3}

    json_serializer = JsonSerializer()
    print(json_serializer.dumps(a))
    print(json_serializer.dumps(b))
    print(json_serializer.dumps(c))
    print(json_serializer.dumps(d))

    z = 5 + 9j
    print(json_serializer.dumps(z))
    print(json_serializer.dumps(g))

    def simple_function(x):
        x = x + math.fabs(A)
        return x ** 2

    def recursive_function(n):
        if n == 0:
            return 1
        else:
            return recursive_function(n - 1) * n

    lambda_expression = lambda x: simple_function(x) + 20

    def closure_function(f):
        bb = 7

        def helper(s):
            return f * s * bb
        return helper

    def generator(x):
        while x:
            if x % 2 == 0:
                yield 'Even'
            x -= 1

    def simple_decorator(func):
        def wrapper(*args):
            print(f"Function {func.__name__} is called with arguments: {args}")
            return func(*args)

        return wrapper

    @simple_decorator
    def my_func(ll):
        return ll + 1

    kom = '{"type": list, "source": [6, 9, "7658675", {89: 89, 69: 89}, {"type": list, "source": [1, 2, 3]}]}'
    print(json_serializer.loads(kom))

    fifi = json_serializer.dumps(simple_function)
    print(fifi)
    new = json_serializer.loads(fifi)
    print(simple_function(5))
    print(new(5))

    fifi = json_serializer.dumps(recursive_function)
    new = json_serializer.loads(fifi)
    print(recursive_function(5))
    print(new(5))

    fifi = json_serializer.dumps(lambda_expression)
    new = json_serializer.loads(fifi)
    print(lambda_expression(5))
    print(new(5))

    fifi = json_serializer.dumps(closure_function)
    new = json_serializer.loads(fifi)
    print(closure_function(5)(2))
    print(new(5)(2))

    fifi = json_serializer.dumps(closure_function(5))
    new = json_serializer.loads(fifi)
    print(closure_function(5)(2))
    print(new(2))

    fifi = json_serializer.dumps(generator)
    new = json_serializer.loads(fifi)
    for i in generator(6):
        print(i)
    for i in new(6):
        print(i)

    def jopa(x):
        print(x)

    fifi = json_serializer.dumps(jopa)
    new = json_serializer.loads(fifi)
    jopa(8)
    new(8)

    fifi = json_serializer.dumps(my_func)
    new = json_serializer.loads(fifi)
    print(my_func(5))
    print(new(5))

    fifi = json_serializer.dumps(simple_decorator)
    new = json_serializer.loads(fifi)

    @new
    def new_func(ll):
        return ll + 1

    new_func(6)

    def fibonacci(n):
        a, b = 0, 1
        for i in range(n):
            yield a
            a, b = b, a + b


    for i in fibonacci(10):
        print(i)

    fifi = json_serializer.dumps(fibonacci)
    new = json_serializer.loads(fifi)

    for i in new(5):
        print(i)


    # my_list = [1, 2, 3, 4, 5]
    # my_iterator = iter(my_list)
    # for element in my_iterator:
    #     print(element)
    # my_iterator = iter(my_list)
    # fifi = json_serializer.dumps(my_iterator)
    # new = json_serializer.loads(fifi)
    #
    # for element in new:
    #     print(element)

    print(json_serializer.dumps(Person))
    person = Person("Alex", 28)

    fifi = json_serializer.dumps(person)
    new_person = json_serializer.loads(fifi)
    print(vars(new_person))

    fifi = json_serializer.dumps(Person)
    JJ = json_serializer.loads(fifi)
    hh = JJ("56", 56)
    print(vars(hh))

    print(JJ.koko(2))
