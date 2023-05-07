import types
from inspect import getmembers
import regex as re
from constants import *

class JsonSerializer:
    def dumps(self, obj):
        if isinstance(obj, PRIMITIVE_TYPES) or obj is None:
            return self._get_primitive_types(obj)
        elif isinstance(obj, types.FunctionType):
            return self._get_function(obj)
        else:
            return self._get_object(obj)

    def dump(self, obj, file_name):
        pass

    def loads(self, str):
        return self._set_primitive_types(str)

    def load(self, file_name):
        pass

    def _get_primitive_types(self, obj):
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
            return f'{{"type": {obj_name}, "source": [{", ".join(self._get_primitive_types(o) for o in obj)}]}}'
        elif isinstance(obj, dict):
            return f'{{{", ".join(f"{self._get_primitive_types(k)}: {self._get_primitive_types(v)}" for k, v in obj.items())}}}'

    def _get_function(self, obj):
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

        return '{' + result + '}'

    def _get_object(self, obj):
        obj_name = obj.__class__.__name__
        attributes = ", ".join(f'"{k}": {self._get_primitive_types(v)}' for k, v in vars(obj).items())

        return f'{{"type": {obj_name}, "source": {{{attributes}}}}}'

    def _set_primitive_types(self, obj):
        if re.fullmatch(BOOL, obj):
            return bool(obj)
        elif re.fullmatch(INT, obj):
            return int(obj)
        elif re.fullmatch(FLOAT, obj):
            return float(obj)
        elif re.fullmatch(COMPLEX, obj):
            return complex(obj)
        elif re.fullmatch(STRING, obj):
            return str(obj[1:-1])
        elif re.fullmatch(NONE, obj):
            return None
        elif re.fullmatch(LIST, obj):
            stack = [el for el in re.findall(LIST_DICT, obj[1:-1])]
            stack = stack[::-1]
            s = '[' + re.sub(LIST_DICT, r'--', obj[1:-1]) + ']'

            result = list()
            for e in re.findall(LIST_ELEM, s):
                if e == '--':
                    result.append(self._set_primitive_types(stack.pop()))
                else:
                    result.append(self._set_primitive_types(e))

            return result

        elif re.fullmatch(DICT, obj):
            if re.match(TYPE, obj):
                t = str(re.match(TYPE, obj).group(1))
                if t in STRING_TYPES:
                    return STRING_TYPES[t](self._set_primitive_types(re.search(SOURCE, obj).group(0)))
            else:
                stack = [el for el in re.findall(LIST_DICT, obj[1:-1])]
                stack = stack[::-1]
                s = '{' + re.sub(LIST_DICT, r'--', obj[1:-1]) + '}'

                result = dict()
                for k, v in zip(re.findall(KEY, s), re.findall(VALUE, s)):
                    if v[1] == '--':
                        result[self._set_primitive_types(k[1])] = self._set_primitive_types(stack.pop())
                    else:
                        result[self._set_primitive_types(k[1])] = self._set_primitive_types(v[1])

                return result







