from types import WrapperDescriptorType, MethodDescriptorType, BuiltinFunctionType, GetSetDescriptorType, MappingProxyType

PRIMITIVE_COLLECTIONS = (list, tuple, set, frozenset, bytes, bytearray)
PRIMITIVE_TYPES = (bool, int, float, str, complex, *PRIMITIVE_COLLECTIONS, dict)

STRING_TYPES = {"list": list, "tuple": tuple, "set": set, "frozenset": frozenset, "bytes": bytes, "bytearray": bytearray}

EXCLUDED_PARAMETERS = ("__name__", "__base__", "__basicsize__", "__dictoffset__", "__class__")
EXCLUDED_TYPES = (WrapperDescriptorType, MethodDescriptorType, BuiltinFunctionType, GetSetDescriptorType, MappingProxyType)

CODE_PROPERTIES = ("co_argcount",         # number of arguments (not including keyword only arguments, * or **args)
                   "co_posonlyargcount",  # number of positional-only arguments
                   "co_kwonlyargcount",   # number of keyword only arguments (not including ** arg)
                   "co_nlocals",          # number of local variables
                   "co_stacksize",        # virtual machine stack space required
                   "co_flags",            # bitmap of CO_* flags, read more here
                   "co_code",             # string of raw compiled bytecode
                   "co_consts",           # tuple of constants used in the bytecode
                   "co_names",            # tuple of names of local variables
                   "co_varnames",         # tuple of names of arguments and local variables
                   "co_filename",         # name of file in which this code object was created
                   "co_name",             # name with which this code object was defined
                   "co_firstlineno",      # number of first line in Python source code
                   "co_lnotab",           # encoded mapping of line numbers to bytecode indices
                   "co_freevars",         # tuple of names of free variables (referenced via a function's closure)
                   "co_cellvars")         # tuple of names of cell variables (referenced by containing scopes)


# --------------------------------------regex expressions------------------------------------------------------

# for json format
BOOL_J = r'true|false'
INT_J = r'[+-]?\d+'
FLOAT_J = r'[+-]?[\d.]+'
COMPLEX_J = r'(?<=\()[\d.+-j]+(?=\))'
NONE_J = r'null'
STRING_J = r'".+"'

LIST_J = r'\[(?:[^\[\]]*|(?R))*\]'
DICT_J = r'{(?:[^{}]*|(?R))*}'
LIST_DICT_J = f'{LIST_J}|{DICT_J}'

TYPE_J = r'^(?:{"type": )(\w+)(?=,)'
SOURCE_J = r'(?<="source": )(.+)(?=})'

KEY_J = r'((?<=, )|(?<={))(.*?)(?=:)'
VALUE_J = r'(?<=:\s)(.*?)(?=[,}])'
LIST_ELEM_J = r'(?<=[\[ ])(.*?)(?=[,\]])'

# for xml format
BOOL_X = r'<bool>(.+)<\/bool>'
INT_X = r'<int>(.+)<\/int>'
FLOAT_X = r'<float>(.+)<\/float>'
STRING_X = r'<str>(.+)<\/str>'
NONE_X = r'<NoneType>(.+)<\/NoneType>'
COMPLEX_X = r'<complex>(.+)<\/complex>'

LIST_X = LIST_J
DICT_X = DICT_J
LIST_DICT_X = LIST_DICT_J

TYPE_X = r'(?:{<key><str>type<\/str><\/key><value>)(\w+)(?=<\/value>)'
SOURCE_X = r'(?<=source<\/str><\/key><value>)([{}\[\]\s.<\w\/>:\\-]+)(?=<\/value>)'

KEY_X = r'(?<=<key>)\s*(<\w+>[{}\[\]\s.<\w\/>]*?<\/\w+>)\s*(?=<\/key)'
VALUE_X = r'(?<=<value>)\s*(<\w+>[:\\{}\[\]\s.<\w\/>-]*?<\/\w+>)\s*(?=<\/value)'
LIST_ELEM_X = r'(<\w+>[{}\[\]\s.<\w\/>-]*?<\/\w+>)'