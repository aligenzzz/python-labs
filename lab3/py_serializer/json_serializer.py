import types
from inspect import getmembers, isclass, isfunction
import regex as re

from py_serializer.constants import PRIMITIVE_COLLECTIONS, \
                                    PRIMITIVE_TYPES, \
                                    STRING_TYPES, \
                                    EXCLUDED_PARAMETERS, EXCLUDED_TYPES, \
                                    CODE_PROPERTIES, \
                                    BOOL_J, INT_J, FLOAT_J, COMPLEX_J, NONE_J, STRING_J, \
                                    LIST_J, DICT_J, LIST_DICT_J, \
                                    TYPE_J, SOURCE_J, \
                                    KEY_J, VALUE_J, LIST_ELEM_J

class JsonSerializer:
    def dumps(self, obj):
        if isinstance(obj, PRIMITIVE_TYPES) or obj is None:
            return self._get_primitive_types(obj)
        elif isinstance(obj, types.FunctionType):
            return self._get_function(obj)
        elif isinstance(obj, types.CodeType):
            return f'{{"type": code, "source": {self.dumps({k: v for k, v in getmembers(obj) if k in CODE_PROPERTIES})}}}'
        elif isinstance(obj, types.CellType):
            return f'{{"type": cell, "source": {self.dumps(obj.cell_contents)}}}'
        # if isinstance(obj, types.ModuleType):
        #     return f'"module {obj.__name__}": {self.dumps(obj.__name__)}'
        elif isclass(obj):
            return self._get_class(obj)
        else:
            return self._get_object(obj)

    def dump(self, obj, file_name):
        with open(file_name, 'w') as file:
            file.write(self.dumps(obj))

    def loads(self, str):
        return self._set_primitive_types(str)

    def load(self, file_name):
        with open(file_name, 'r') as file:
            return self.loads(file.read())

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
            return f'{{"type": {obj_name}, "source": [{", ".join(self.dumps(o) for o in obj)}]}}'
        elif isinstance(obj, dict):
            return f'{{{", ".join(f"{self.dumps(k)}: {self.dumps(v)}" for k, v in obj.items())}}}'

    def _get_function(self, obj):
        obj_name = obj.__class__.__name__
        code = self.dumps(obj.__code__)
        globales = self._get_globals(obj)
        name = obj.__name__
        defaults = obj.__defaults__
        closure = obj.__closure__

        result = f'{{"type": {obj_name}, "source": {{' \
                 f'"code": {code}, ' \
                 f'"globals": {globales}, ' \
                 f'"name": {self.dumps(name)}, ' \
                 f'"defaults": {self.dumps(defaults)}, ' \
                 f'"closure": {self.dumps(closure)}}}}}'

        return result

    def _get_globals(self, obj):
        result = ''

        for element in obj.__code__.co_names:
            if element in obj.__globals__:
                if isinstance(obj.__globals__[element], types.ModuleType):
                    module = obj.__globals__[element].__name__
                    result += f'"module {module}": {self.dumps(module)}, '
                elif element != obj.__code__.co_name:
                    result += f'"{element}": {self.dumps(obj.__globals__[element])}, '
                else:
                    result += f'"{element}": {self.dumps(obj.__name__)}, '

        if result != '':
            result = result[:-2]

        return '{' + result + '}'

    def _get_class(self, obj):
        source = ''
        source += f'"__name__": "{obj.__name__}", '

        obj_dict = obj.__dict__
        for key in obj_dict:
            member = obj_dict[key]

            if key in EXCLUDED_PARAMETERS or type(member) in EXCLUDED_TYPES:
                continue

            if isinstance(obj_dict[key], (staticmethod, classmethod)):
                source += f'"{key}": {self._get_function(member.__func__)}, '
            elif isinstance(obj_dict[key], property):
                value = dict()
                value["fget"] = member.fget
                value["fset"] = member.fset
                value["fdel"] = member.fdel
                value["doc"] = member.__doc__
                source += f'"{key}": {{"type": property, "source": {self.dumps(value)}}}, '
            elif isfunction(member):
                source += f'"{key}": {self._get_function(member)}, '
            else:
                source += f'"{key}": {self.dumps(member)}, '

        source += f'"__bases__": {self.dumps(tuple([base for base in obj.__bases__ if base != object]))}'

        return f'{{"type": class, "source": {{{source}}}}}'

    def _get_object(self, obj):
        members = ", ".join(f'"{k}": {self._get_primitive_types(v)}' for k, v in vars(obj).items())
        class_source = self.dumps(obj.__class__)

        return f'{{"type": object, "source": ' \
               f'{{"class": {class_source}, ' \
               f'"members": {{{members}}}}}}}'

    def _set_primitive_types(self, obj):
        if re.fullmatch(BOOL_J, obj):
            return bool(obj)
        elif re.fullmatch(INT_J, obj):
            return int(obj)
        elif re.fullmatch(FLOAT_J, obj):
            return float(obj)
        elif re.fullmatch(COMPLEX_J, obj):
            return complex(obj)
        elif re.fullmatch(STRING_J, obj):
            return str(obj[1:-1])
        elif re.fullmatch(NONE_J, obj):
            return None
        elif re.fullmatch(LIST_J, obj):
            stack = [el for el in re.findall(LIST_DICT_J, obj[1:-1])]
            stack = stack[::-1]
            raw_str = '[' + re.sub(LIST_DICT_J, r'--', obj[1:-1]) + ']'

            result = list()
            for e in re.findall(LIST_ELEM_J, raw_str):
                if e == '':
                    return result
                elif e == '--':
                    result.append(self._set_primitive_types(stack.pop()))
                else:
                    result.append(self._set_primitive_types(e))

            return result

        elif re.fullmatch(DICT_J, obj):
            if re.match(TYPE_J, obj):
                tipo = str(re.match(TYPE_J, obj).group(1))
                if tipo in STRING_TYPES:
                    return STRING_TYPES[tipo](self._set_primitive_types(re.search(SOURCE_J, obj).group(0)))
                elif tipo == "function":
                    function = self._set_function(re.search(SOURCE_J, obj).group(0))
                    return function
                elif tipo == "code":
                    code = self._set_primitive_types(re.search(SOURCE_J, obj).group(0))
                    return types.CodeType(*[code[p] for p in CODE_PROPERTIES])
                elif tipo == "cell":
                    cell = self._set_primitive_types(re.search(SOURCE_J, obj).group(0))
                    return types.CellType(cell)
                elif tipo == "class":
                    return self._set_class(re.search(SOURCE_J, obj).group(0))
                elif tipo == "object":
                    return self._set_object(re.search(SOURCE_J, obj).group(0))
                elif tipo == "property":
                    value = self.loads(re.search(SOURCE_J, obj).group(0))
                    return property(fget=value["fget"], fset=value["fset"], fdel=value["fdel"], doc=value["doc"])
            else:
                stack = [elem for elem in re.findall(LIST_DICT_J, obj[1:-1])]
                stack = stack[::-1]
                raw_str = '{' + re.sub(LIST_DICT_J, r'--', obj[1:-1]) + '}'

                result = dict()
                for k, v in zip(re.findall(KEY_J, raw_str), re.findall(VALUE_J, raw_str)):
                    if v == '--':
                        result[self._set_primitive_types(k[1])] = self._set_primitive_types(stack.pop())
                    else:
                        result[self._set_primitive_types(k[1])] = self._set_primitive_types(v)

                return result

    def _set_function(self, obj):
        source = self._set_primitive_types(obj)

        code = source["code"]
        globales = source["globals"]
        name = source["name"]
        defaults = source["defaults"]
        clausura = source["closure"]

        temp = dict()
        for k, v in globales.items():
            if re.match(r'module', k):
                temp[v] = __import__(v)
            else:
                temp[k] = v

        # prior to version 3.10, for some reason, he does not import the following built-in modules
        temp['__builtins__'] = __import__('builtins')
        temp['sys'] = __import__('sys')

        globales = temp

        result = types.FunctionType(code, globales, name, defaults, clausura)
        # for recursion
        result.__globals__.update({result.__name__: result})

        return result

    def _set_class(self, obj):
        obj = self._set_primitive_types(obj)
        bases = obj["__bases__"]

        members = dict()
        for k, v in obj.items():
            members[k] = v

        result = type(obj["__name__"], bases, members)

        for k, v in members.items():
            if isfunction(v):
                v.__globals__.update({result.__name__: result})
            elif isinstance(v, (staticmethod, classmethod)):
                v.__func__.__globals__.update({result.__name__: result})

        return result

    def _set_object(self, obj):
        obj = self._set_primitive_types(obj)
        class_source = obj["class"]

        members = dict()
        for k, v in obj["members"].items():
            members[k] = v

        result = object.__new__(class_source)
        result.__dict__ = members

        return result
