
from xml_serializer import XmlSerializer
from tests.data_test import Person

if __name__ == '__main__':
    xml_serializer = XmlSerializer()
    person = Person("Alex", 26)
    p = xml_serializer.dumps(person)
    print(p)
    print(xml_serializer.loads(p))
