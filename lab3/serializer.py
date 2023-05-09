from json_serializer import JsonSerializer
from xml_serializer import XmlSerializer


class Serializer:

    @staticmethod
    def create_serializer(serializer):
        if serializer == "json":
            return JsonSerializer()
        elif serializer == "xml":
            return XmlSerializer()
        else:
            raise ValueError