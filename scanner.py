from enum import Enum, auto

from tokentype import TokenType


# Scanner State
class State(Enum):
    NONE = auto()
    DIGIT = auto()
    ALPHA = auto()


# Lexical Analyzer
class Scanner:
    def __init__(self, code: str):
        self.code = code
        self.state: State = State.NONE
        self.buffer = []
        self.tokens: [TokenType, str] = []
        self.scan_tokens()

    def add_token(self, token_type: TokenType, value: str):
        self.tokens.append((token_type, value))

    def scan_tokens(self):
        for c in self.code:
            if c.isdigit():
                if self.state == State.ALPHA:
                    self.consume_alpha()
                self.buffer.append(c)
                self.state = State.DIGIT
            elif c.isalpha():
                if self.state == State.DIGIT:
                    self.consume_number()
                self.buffer.append(c)
                self.state = State.ALPHA
            else:
                if self.state == State.ALPHA:
                    self.consume_alpha()
                elif self.state == State.DIGIT:
                    self.consume_number()
                self.state = State.NONE
                if c in ['(', ')']:
                    self.add_token(TokenType.PARENTHESES, c)
                elif c in ['{', '}']:
                    self.add_token(TokenType.BRACKET, c)
                elif c in ['<', '+', '*', '=']:
                    self.add_token(TokenType.OPERATOR, c)
                elif c in [';']:
                    self.add_token(TokenType.SEMICOLON, c)

    def consume_alpha(self):
        word = ''.join(self.buffer)
        if word in ['int', 'char']:
            self.add_token(TokenType.TYPE, word)
        elif word in ['IF', 'THEN', 'ELSE']:
            self.add_token(TokenType.STATEMENT, word)
        elif word in ['EXIT']:
            self.add_token(TokenType.EXIT, word)
        else:
            self.add_token(TokenType.WORD, word)
        self.buffer.clear()

    def consume_number(self):
        num = int(''.join(self.buffer))
        self.add_token(TokenType.NUMBER, num)
        self.buffer.clear()

    def print_tokens(self):
        for t in self.tokens:
            print(f"<{t[0].name}, '{t[1]}'>")
