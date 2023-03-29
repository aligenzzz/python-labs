from re import compile

# regex expressions
SENTENCE = compile(r'(?<!A\.D\.)(?<!a\.m\.)(?<!p\.m\.)(?<!Dr\.)(?<!Jr\.)(?<!Sr\.)(?<!St\.)'
                   r'(?<!Prof\.)(?<!Mrs\.)(?<!Mr\.)(?<!Ms\.)(?<!Ave\.)'
                   r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<![A-Z]\.)(?<=[.?!])\s*(?!",?\s?[a-z]|\'|\.)(?=[A-Z"])')
WORD = compile(r'^[\W\d]|\b[^\w\']+\b')


