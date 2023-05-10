import types
from inspect import getmembers, isclass, isfunction
import regex as re

from py_serializer.constants import PRIMITIVE_COLLECTIONS, \
                                    PRIMITIVE_TYPES, \
                                    STRING_TYPES, \
                                    EXCLUDED_PARAMETERS, EXCLUDED_TYPES, \
                                    CODE_PROPERTIES, \
                                    BOOL_X, INT_X, FLOAT_X, COMPLEX_X, NONE_X, STRING_X, \
                                    LIST_X, DICT_X, LIST_DICT_X, \
                                    TYPE_X, SOURCE_X, \
                                    KEY_X, VALUE_X, LIST_ELEM_X

class XmlSerializer:
    def dumps(self, obj):
        if isinstance(obj, PRIMITIVE_TYPES) or obj is None:
            return self._get_primitive_types(obj)
        elif isinstance(obj, types.FunctionType):
            return self._get_function(obj)
        elif isinstance(obj, types.CodeType):
            return f'<dict><key>{self.dumps("type")}</key><value>code</value>' \
                   f'<key>{self.dumps("source")}</key>' \
                   f'<value>{self.dumps({k: v for k, v in getmembers(obj) if k in CODE_PROPERTIES})}</value></dict>'
        elif isinstance(obj, types.CellType):
            return f'<dict><key>{self.dumps("type")}</key><value>cell</value>' \
                   f'<key>{self.dumps("source")}</key><value>{self.dumps(obj.cell_contents)}</value></dict>'
        elif isclass(obj):
            return self._get_class(obj)
        else:
            return self._get_object(obj)

    def dump(self, obj, file_name):
        with open(file_name, 'w') as file:
            file.write(self.dumps(obj))

    def loads(self, str):
        str = re.sub(r'<list>', '[', str)
        str = re.sub(r'</list>', ']', str)
        str = re.sub(r'<dict>', '{', str)
        str = re.sub(r'</dict>', '}', str)

        return self._set_primitive_types(str)

    def load(self, file_name):
        with open(file_name, 'r') as file:
            return self.loads(file.read())

    def _get_primitive_types(self, obj):
        obj_name = obj.__class__.__name__

        if isinstance(obj, bool):
            return f'<{obj_name}>{str(obj).lower()}</{obj_name}>'
        elif isinstance(obj, (int, float, str, complex)) or obj is None:
            return f'<{obj_name}>{obj}</{obj_name}>'
        elif isinstance(obj, list):
            return f'<list>{"".join(self.dumps(o) for o in obj)}</list>'
        elif isinstance(obj, dict):
            return f'<dict>{"".join(f"<key>{self.dumps(k)}</key><value>{self.dumps(v)}</value>" for k, v in obj.items())}</dict>'
        elif isinstance(obj, PRIMITIVE_COLLECTIONS):
            return f'<dict><key>{self.dumps("type")}</key><value>{obj_name}</value>' \
                   f'<key>{self.dumps("source")}</key><value><list>{"".join(self.dumps(o) for o in obj)}</list></value></dict>'

    def _get_function(self, obj):
        obj_name = obj.__class__.__name__
        code = self.dumps(obj.__code__)
        globales = self._get_globals(obj)
        name = obj.__name__
        defaults = obj.__defaults__
        closure = obj.__closure__

        result = f'<dict><key>{self.dumps("type")}</key><value>{obj_name}</value>' \
                 f'<key>{self.dumps("source")}</key><value><dict>' \
                 f'<key>{self.dumps("code")}</key><value>{code}</value>' \
                 f'<key>{self.dumps("globals")}</key><value>{globales}</value>' \
                 f'<key>{self.dumps("name")}</key><value>{self.dumps(name)}</value>' \
                 f'<key>{self.dumps("defaults")}</key><value>{self.dumps(defaults)}</value>' \
                 f'<key>{self.dumps("closure")}</key><value>{self.dumps(closure)}</value></dict></value></dict>'

        return result

    def _get_globals(self, obj):
        result = ''

        for element in obj.__code__.co_names:
            if element in obj.__globals__:
                if isinstance(obj.__globals__[element], types.ModuleType):
                    module = obj.__globals__[element].__name__
                    result += f'<key>{self.dumps("module " + str(module))}</key><value>{self.dumps(module)}</value>'
                elif element != obj.__code__.co_name:
                    result += f'<key>{self.dumps(str(element))}</key><value>{self.dumps(obj.__globals__[element])}</value>'
                else:
                    result += f'<key>{self.dumps(str(element))}</key><value>{self.dumps(obj.__name__)}</value>'

        return '<dict>' + result + '</dict>'

    def _get_class(self, obj):
        source = ''
        source += f'<key>{self.dumps("__name__")}</key><value>{self.dumps(str(obj.__name__))}</value>'

        obj_dict = obj.__dict__
        for key in obj_dict:
            member = obj_dict[key]

            if key in EXCLUDED_PARAMETERS or type(member) in EXCLUDED_TYPES:
                continue

            if isinstance(obj_dict[key], (staticmethod, classmethod)):
                source += f'<key>{self.dumps(key)}</key><value>{self._get_function(member.__func__)}</value>'
            elif isinstance(obj_dict[key], property):
                value = dict()
                value["fget"] = member.fget
                value["fset"] = member.fset
                value["fdel"] = member.fdel
                value["doc"] = member.__doc__
                source += f'<key>{self.dumps(key)}</key><value><dict>' \
                          f'<key>{self.dumps("type")}</key><value>property</value>' \
                          f'<key>{self.dumps("source")}</key><value>{self.dumps(value)}</value></dict></value>'
            elif isfunction(member):
                source += f'<key>{self.dumps(key)}</key><value>{self._get_function(member)}</value>'
            else:
                source += f'<key>{self.dumps(key)}</key><value>{self.dumps(member)}</value>'

        source += f'<key>{self.dumps("__bases__")}</key>' \
                  f'<value>{self.dumps(tuple([base for base in obj.__bases__ if base != object]))}</value>'

        return f'<dict><key>{self.dumps("type")}</key><value>class</value>' \
               f'<key>{self.dumps("source")}</key><value><dict>{source}</dict></value></dict>'

    def _get_object(self, obj):
        members = "".join(f'<key>{self.dumps(str(k))}</key><value>{self.dumps(v)}</value>' for k, v in vars(obj).items())
        class_source = self.dumps(obj.__class__)

        return f'<dict><key>{self.dumps("type")}</key><value>object</value>' \
               f'<key>{self.dumps("source")}</key><value><dict>' \
               f'<key>{self.dumps("class")}</key><value>{class_source}</value>' \
               f'<key>{self.dumps("members")}</key><value><dict>{members}</dict>' \
               f'</value></dict></value></dict>'

    def _set_primitive_types(self, obj):
        if re.match(BOOL_X, obj):
            value = re.match(BOOL_X, obj)[1]
            return bool(value)
        elif re.match(INT_X, obj):
            value = re.match(INT_X, obj)[1]
            return int(value)
        elif re.match(FLOAT_X, obj):
            value = re.match(FLOAT_X, obj)[1]
            return float(value)
        elif re.match(COMPLEX_X, obj):
            value = re.match(COMPLEX_X, obj)[1]
            return complex(value)
        elif re.match(STRING_X, obj):
            value = re.match(STRING_X, obj)[1]
            return str(value)
        elif re.match(NONE_X, obj):
            return None
        elif re.match(LIST_X, obj):
            stack = [el for el in re.findall(LIST_DICT_X, obj[1:-1])]
            stack = stack[::-1]
            raw_str = '[' + re.sub(LIST_DICT_X, r'<s>--</s>', obj[1:-1]) + ']'

            result = list()
            for e in re.findall(LIST_ELEM_X, raw_str):
                if e == '':
                    return result
                elif e == '<s>--</s>':
                    result.append(self._set_primitive_types(stack.pop()))
                else:
                    result.append(self._set_primitive_types(e))

            return result

        elif re.match(DICT_X, obj):
            if re.match(TYPE_X, obj):
                tipo = str(re.match(TYPE_X, obj).group(1))
                if tipo in STRING_TYPES:
                    return STRING_TYPES[tipo](self._set_primitive_types(re.search(SOURCE_X, obj).group(1)))
                elif tipo == "function":
                    function = self._set_function(re.search(SOURCE_X, obj).group(1))
                    return function
                elif tipo == "code":
                    code = self._set_primitive_types(re.search(SOURCE_X, obj).group(1))
                    return types.CodeType(*[code[p] for p in CODE_PROPERTIES])
                elif tipo == "cell":
                    cell = self._set_primitive_types(re.search(SOURCE_X, obj).group(1))
                    return types.CellType(cell)
                elif tipo == "class":
                    return self._set_class(re.search(SOURCE_X, obj).group(1))
                elif tipo == "object":
                    return self._set_object(re.search(SOURCE_X, obj).group(1))
                elif tipo == "property":
                    value = self.loads(re.search(SOURCE_X, obj).group(1))
                    return property(fget=value["fget"], fset=value["fset"], fdel=value["fdel"], doc=value["doc"])
            else:
                stack = [el for el in re.findall(LIST_DICT_X, obj[1:-1])]
                stack = stack[::-1]
                raw_str = '{' + re.sub(LIST_DICT_X, r'<s>--</s>', obj[1:-1]) + '}'

                result = dict()
                for k, v in zip(re.findall(KEY_X, raw_str), re.findall(VALUE_X, raw_str)):
                    if v == '<s>--</s>':
                        result[self._set_primitive_types(k)] = self._set_primitive_types(stack.pop())
                    else:
                        result[self._set_primitive_types(k)] = self._set_primitive_types(v)

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
