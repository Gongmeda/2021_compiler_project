import sys


# LL(1) Parser
class LLParser:
    def __init__(self, tokens, grammar_path):
        self.tokens = tokens
        self.grammar = self.parse_grammar(grammar_path)
        self.first = self.get_first()
        self.follow = self.get_follow()
        self.parsing_table = None

    def parse_grammar(self, grammar_path):
        # 문법 파일 파싱
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

        # LL Grammar 생성
        # 1. left-factoring
        grammar = self.left_factoring(grammar)

        # 2. left-recursion 제거
        grammar = self.remove_left_recursion(grammar)

        return grammar

    def left_factoring(self, grammar: dict):
        keys = list(grammar.keys())
        for i in range(len(keys)):
            helper_name = keys[i] + "'"
            has_prefix = True
            while has_prefix:
                has_prefix = False
                longest = []
                generation = grammar[keys[i]]
                for j in range(len(generation)):
                    for k in range(j + 1, len(generation)):
                        l = 0
                        while l < len(generation[j]) and l < len(generation[k]):
                            if generation[j][l] != generation[k][l]:
                                break
                            l = l + 1
                        if l > 0:
                            has_prefix = True
                            if l > len(longest):
                                longest = generation[j][:l]
                if has_prefix:
                    while helper_name in grammar:
                        helper_name = helper_name + "'"
                    grammar[helper_name] = []
                    j = 0
                    for k in range(len(generation)):
                        if len(generation[k]) >= len(longest) and generation[k][:len(longest)] == longest:
                            if len(generation[k]) == len(longest):
                                grammar[helper_name].append([])
                            else:
                                grammar[helper_name].append(generation[k][len(longest):])
                        else:
                            grammar[keys[i]][j] = grammar[keys[i]][k]
                            j = j + 1
                    grammar[keys[i]] = [[*longest, helper_name]] + grammar[keys[i]][:j]

        return grammar

    def remove_left_recursion(self, grammar):
        return grammar

    def print_grammar(self):
        print("==== PARSED LL GRAMMAR ====")
        for k, kv in self.grammar.items():
            print(f"{k:<10} ::= ", end='')
            for i, iv in enumerate(kv):
                rule = ' '.join(iv)
                if i == 0:
                    print(rule)
                elif i == len(kv) - 1:
                    print(' ' * 13 + f"| {rule} ;")
                else:
                    print(' ' * 13 + f"| {rule}")
        print()

    def get_first(self):
        pass

    def get_follow(self):
        pass
