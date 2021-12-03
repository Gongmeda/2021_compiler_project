from enum import Enum, auto


class TokenType(Enum):
    PARENTHESES = auto()    # ['(', ')']
    BRACKET = auto()        # ['{', '}']
    OPERATOR = auto()       # ['<', '+', '*', '=']
    SEMICOLON = auto()      # [';']
    TYPE = auto()           # ['int', 'char']
    STATEMENT = auto()      # ['IF', 'THEN', 'ELSE']
    EXIT = auto()           # ['EXIT']
    WORD = auto()           # ([a-z] | [A-Z])*
    NUMBER = auto()         # [0-9]*
