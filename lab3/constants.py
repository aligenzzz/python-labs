
PRIMITIVE_COLLECTIONS = (list, tuple, set, frozenset, bytes, bytearray)
PRIMITIVE_TYPES = (bool, int, float, str, complex, *PRIMITIVE_COLLECTIONS, dict)

STRING_TYPES = {"list": list, "tuple": tuple, "set": set, "frozenset": frozenset, "bytes": bytes, "bytearray": bytearray}

FUNCTION_PROPERTIES = ("co_argcount",   # number of arguments (not including keyword only arguments, * or **args)
                       "co_code",       # string of raw compiled bytecode
                       "co_cellvars",   # tuple of names of cell variables (referenced by containing scopes)
                       "co_consts",     # tuple of constants used in the bytecode
                       "co_filename",   # name of file in which this code object was created
                       "co_firstlineno",  # number of first line in Python source code
                       "co_flags",      # bitmap of CO_* flags, read more here
                       "co_lnotab",     # encoded mapping of line numbers to bytecode indices
                       "co_freevars",   # tuple of names of free variables (referenced via a function's closure)
                       "co_kwonlyargcount",  # number of keyword only arguments (not including ** arg)
                       "co_name",       # name with which this code object was defined
                       "co_names",      # tuple of names of local variables
                       "co_nlocals",     # number of local variables
                       "co_stacksize",   # virtual machine stack space required
                       "co_varnames")    # tuple of names of arguments and local variables

# regex expressions
BOOL = r'true|false'
INT = r'[+-]?\d+'
FLOAT = r'[+-]?[\d.]+'
COMPLEX = r'(?<=\()[\d.+-j]+(?=\))'
NONE = r'null'
STRING = r'".+"'

LIST = r'\[(?:.)*\]'
DICT = r'{(?:[^{}]*|(?R))*}'
LIST_DICT = f'{LIST}|{DICT}'

TYPE = r'^(?:{"type": )(\w+)(?=,)'
SOURCE = r'(?<="source": )(.+)(?=})'

KEY = r'((?<=, )|(?<={))(.*?)(?=:)'
VALUE = r'(?<=:\s)(.*?)(?=[,}])'

LIST_ELEM = r'(?<=[\[ ])(.*?)(?=[,\]])'

