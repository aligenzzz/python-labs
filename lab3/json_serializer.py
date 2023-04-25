import types
from inspect import getmembers
from constants import PRIMITIVE_COLLECTIONS, PRIMITIVE_TYPES, FUNCTION_PROPERTIES

class JsonSerializer:
    def dumps(self, obj):
        if isinstance(obj, PRIMITIVE_TYPES) or obj is None:
            return self._serialize_primitive_types(obj)
        elif isinstance(obj, types.FunctionType):
            return self._serialize_function(obj)

    def dump(self, obj, file_name):
        pass

    def loads(self, str):
        pass

    def load(self, file_name):
        pass

    def _serialize_primitive_types(self, obj):
        obj_name = obj.__class__.__name__

        if isinstance(obj, bool):
            return str(obj).lower()
        elif isinstance(obj, (int, float)):
            return str(obj)
        elif isinstance(obj, str):
            return f'"{obj}"'
        elif obj is None:
            return 'null'
        elif isinstance(obj, complex):
            return f'{{"type": {obj_name}, "source": {obj}}}'
        elif isinstance(obj, PRIMITIVE_COLLECTIONS):
            return f'{{"type": {obj_name}, "source": [{", ".join(self._serialize_primitive_types(o) for o in obj)}]}}'
        elif isinstance(obj, dict):
            return f'{{{", ".join(f"{self._serialize_primitive_types(k)}: {self._serialize_primitive_types(v)}" for k, v in obj.items())}}}'

    def _serialize_function(self, obj):
        obj_name = obj.__class__.__name__
        code = {k: v for k, v in getmembers(obj.__code__) if k in FUNCTION_PROPERTIES}
        globals_ = self._get_globals(obj)
        name = obj.__name__
        defaults = obj.__defaults__
        closure = obj.__closure__

        result = f'{{"type": {obj_name}, "source": {{' \
                 f'"code": {self.dumps(code)}, ' \
                 f'"globals": {globals_}, ' \
                 f'"name": {self.dumps(name)}, ' \
                 f'"defaults": {self.dumps(defaults)}, ' \
                 f'"closure": {self.dumps(closure)} }}}}'

        return result

    def _get_globals(self, obj):
        result = ''

        for element in obj.__code__.co_names:
            if element in obj.__globals__:
                if isinstance(obj.__globals__[element], types.ModuleType):
                    result += f'"{element}": {self.dumps(obj.__globals__[element].__name__)}, '
                elif element != obj.__code__.co_name:
                    result += f'"{element}": {self.dumps(obj.__globals__[element])}, '
                else:
                    result += f'"{element}": {self.dumps(obj.__name__)}, '

        if result != '':
            result = result[:-2]

        return result

    def _get_object(self, obj):
        pass

    def _deserialize_primitive_types(self, obj):
        pass







