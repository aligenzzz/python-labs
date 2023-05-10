import math

a = 6

primitive = [6, 9, "7658675", {89: 89, 69: 89}, [1, 2, 3]]


def simple_function(x):
    x = x + math.fabs(a)
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
        print(f"arguments{args}")
        return func(*args)

    return wrapper


@simple_decorator
def my_func(p):
    return p + 1


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @staticmethod
    def koko(x):
        return x * 2

    def instancemethod(self):
        return 'instance method called', self

    @classmethod
    def classmethod(cls):
        return 'class method called', cls

    @staticmethod
    def staticmethod():
        return 'static method called'

    def fact(self, n):
        if n == 0:
            return 1
        else:
            return self.fact(n - 1) * n

class A:
    x = 15

    def __init__(self) -> None:
        self.f = 12
        self.b = 10

    def my_meth(self):
        return self.f * self.b

class B(A):
    pass

person = Person("Alex", 26)
