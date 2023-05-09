import unittest

from py_serializer.serializer import Serializer
from data_test import primitive, \
                      simple_function, \
                      recursive_function, \
                      lambda_expression, \
                      closure_function, \
                      generator, \
                      simple_decorator, \
                      my_func, \
                      Person, person, \
                      A, B

xml_serializer = Serializer.create_serializer("xml")

class MyTestCase(unittest.TestCase):
    def test_primitive_types_serialization(self):
        expected = primitive
        actual = xml_serializer.loads(xml_serializer.dumps(primitive))
        self.assertEqual(expected, actual)

    def test_simple_function_serialization(self):
        expected = simple_function(10)
        actual = xml_serializer.loads(xml_serializer.dumps(simple_function))(10)
        self.assertEqual(expected, actual)

    def test_recursive_function_serialization(self):
        expected = recursive_function(10)
        actual = xml_serializer.loads(xml_serializer.dumps(recursive_function))(10)
        self.assertEqual(expected, actual)

    def test_lambda_expression_serialization(self):
        expected = lambda_expression(10)
        actual = xml_serializer.loads(xml_serializer.dumps(lambda_expression))(10)
        self.assertEqual(expected, actual)

    def test_closure_function_serialization(self):
        expected = closure_function(5)(6)

        actual = xml_serializer.loads(xml_serializer.dumps(closure_function))(5)(6)
        self.assertEqual(expected, actual)

        actual = xml_serializer.loads(xml_serializer.dumps(closure_function(5)))(6)
        self.assertEqual(expected, actual)

    def test_generator_serialization(self):
        expected = ''
        for i in generator(6):
            expected += i

        actual = ''
        for i in xml_serializer.loads(xml_serializer.dumps(generator))(6):
            actual += i

        self.assertEqual(expected, actual)

    def test_decorator_serialization(self):
        expected = my_func(6)

        actual = xml_serializer.loads(xml_serializer.dumps(my_func))(6)
        self.assertEqual(expected, actual)

        new = xml_serializer.loads(xml_serializer.dumps(simple_decorator))

        @new
        def func(p):
            return p + 1

        actual = func(6)
        self.assertEqual(expected, actual)

    def test_class_methods_serialization(self):
        new = xml_serializer.loads(xml_serializer.dumps(person))
        New = xml_serializer.loads(xml_serializer.dumps(Person))

        expected = person.instancemethod()[0]
        actual = new.instancemethod()[0]
        self.assertEqual(expected, actual)

        expected = Person.koko(5)
        actual = New.koko(5)
        self.assertEqual(expected, actual)

        expected = person.classmethod()[0]
        actual = new.classmethod()[0]
        self.assertEqual(expected, actual)

        expected = person.fact(10)
        actual = new.fact(10)
        self.assertEqual(expected, actual)

    def test_class_serialization(self):
        expected = A.x
        actual = xml_serializer.loads(xml_serializer.dumps(A)).x
        self.assertEqual(expected, actual)

        expected = B.x
        actual = xml_serializer.loads(xml_serializer.dumps(B)).x
        self.assertEqual(expected, actual)

    def test_object_serialization(self):
        expected = vars(person)
        actual = vars(xml_serializer.loads(xml_serializer.dumps(person)))
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
