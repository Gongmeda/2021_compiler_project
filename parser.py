import sys


class Parser:
    def __init__(self, tokens, grammar_path):
        self.tokens = tokens
        self.grammar = self.parse_grammar(grammar_path)
        self.first = self.get_first()
        self.follow = self.get_follow()
        self.parsing_table = None

    def parse_grammar(self, grammar_path):
        try:
            grammar = {}
            with open(f'./{grammar_path}', 'r') as file:
                rules = list(map(str.strip, file.read().split(' ;')))
                rules.pop(-1)
                for r in rules:
                    key, value = map(str.strip, r.split('::='))
                    grammar[key] = list(map(str.split, (map(str.strip, value.split('|')))))
        except IOError:
            sys.exit("Parser Error: invalid grammar file path")
        return grammar

    def print_grammar(self):
        print("==== PARSED GRAMMAR ====")
        for k, kv in self.grammar.items():
            print(f"{k:<10} ::= ", end='')
            for i, iv in enumerate(kv):
                if i == 0:
                    print(' '.join(iv))
                elif i == len(kv) - 1:
                    print(' ' * 13 + f"| {' '.join(iv)} ;")
                else:
                    print(' ' * 13 + f"| {' '.join(iv)}")
        print()

    def get_first(self):
        pass

    def get_follow(self):
        pass
        

