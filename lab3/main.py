from json_serializer import JsonSerializer
import math

A = 6

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

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

    def my_func(x):
        x = x + math.fabs(A)
        return x ** 2

    person = Person("pam", 56)
    print(vars(person))
    print(dir(person))

    fifi = json_serializer.dumps(my_func)
    print(fifi)
    print(json_serializer.dumps(person))

    kkkkk = '{"type": list, "source": [6, 9, "7658675", {89: 89, 69: 89}, {"type": list, "source": [1, 2, 3]}]}'
    print(json_serializer.loads(kkkkk))

    new = json_serializer.loads(fifi)
    print(new(5))
    print(my_func(5))
