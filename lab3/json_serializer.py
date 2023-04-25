import types
from constants import PRIMITIVE_COLLECTIONS, PRIMITIVE_TYPES

class JsonSerializer:

    def dumps(self, obj):
        if isinstance(obj, PRIMITIVE_TYPES) or obj is None:
            return self._get_primitive_types(obj)

    def dump(self, obj, file_name):
        pass

    def loads(self, str):
        pass

    def load(self, file_name):
        pass

    def _get_primitive_types(self, obj):
        if isinstance(obj, bool):
            return str(obj).lower()
        elif isinstance(obj, (int, float)):
            return str(obj)
        elif isinstance(obj, str):
            return '"' + obj + '"'
        elif obj is None:
            return 'null'
        elif isinstance(obj, complex):
            return '{' + f'"type": {obj.__class__.__name__}, "source": {obj}' + '}'
        elif isinstance(obj, PRIMITIVE_COLLECTIONS):
            return '{' + f'"type": {obj.__class__.__name__}, "source": [' + ', '.join(self._get_primitive_types(element)
                                                                                      for element in obj) + ']' + '}'
        elif isinstance(obj, dict):
            return '{' + ', '.join(f'"{key}": {self._get_primitive_types(value)}'
                                   for key, value in obj.items()) + '}'
        else:
            raise Exception(f'Object of type {obj.__class__.__name__} is not JSON serializable!')

    def _get_function(self, obj):
        pass

    def _get_object(self, obj):
        pass







