from types import WrapperDescriptorType, MethodDescriptorType, BuiltinFunctionType, GetSetDescriptorType, MappingProxyType

PRIMITIVE_COLLECTIONS = (list, tuple, set, frozenset, bytes, bytearray)
PRIMITIVE_TYPES = (bool, int, float, str, complex, *PRIMITIVE_COLLECTIONS, dict)

STRING_TYPES = {"list": list, "tuple": tuple, "set": set, "frozenset": frozenset, "bytes": bytes, "bytearray": bytearray}

EXCLUDED_PARAMETERS = ("__name__", "__base__", "__basicsize__", "__dictoffset__", "__class__")
EXCLUDED_TYPES = (WrapperDescriptorType, MethodDescriptorType, BuiltinFunctionType, GetSetDescriptorType, MappingProxyType)
CODE_PROPERTIES = ("co_argcount",         # number of arguments (not including keyword only arguments, * or **args)
                   "co_posonlyargcount",  #
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

# regex expressions
BOOL = r'true|false'
INT = r'[+-]?\d+'
FLOAT = r'[+-]?[\d.]+'
COMPLEX = r'(?<=\()[\d.+-j]+(?=\))'
NONE = r'null'
STRING = r'".+"'

LIST = r'\[(?:[^\[\]]*|(?R))*\]'
DICT = r'{(?:[^{}]*|(?R))*}'
LIST_DICT = f'{LIST}|{DICT}'

TYPE = r'^(?:{"type": )(\w+)(?=,)'
SOURCE = r'(?<="source": )(.+)(?=})'

KEY = r'((?<=, )|(?<={))(.*?)(?=:)'
VALUE = r'(?<=:\s)(.*?)(?=[,}])'

LIST_ELEM = r'(?<=[\[ ])(.*?)(?=[,\]])'
