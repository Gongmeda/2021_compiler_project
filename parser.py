import sys


# LL(1) Parser
class LLParser:
    def __init__(self, tokens, grammar_path):
        self.tokens = tokens
        self.grammar = self.parse_grammar(grammar_path)
        self.nonterminals = list(self.grammar.keys())
        self.terminals = self.get_terminals()
        self.first = self.find_first()
        self.follow = self.find_follow()
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
                    if key == 'word' or key == 'num':
                        exps = [[value]]
                    else:
                        exps = [e.split() for e in list(map(str.strip, value.split('|')))]
                    for i in range(len(exps)):
                        for j in range(len(exps[i])):
                            exps[i][j] = exps[i][j].strip('\"')
                        if not exps[i]:
                            exps[i] = ['']
                    grammar[key] = exps
        except IOError:
            sys.exit("Parser Error: invalid grammar file path")

        # LL Grammar 생성
        # 1. left-factoring
        grammar = self.left_factoring(grammar)

        # 2. left-recursion 제거
        grammar = self.remove_left_recursion(grammar)

        return grammar

    @staticmethod
    def left_factoring(grammar: dict):
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
                                grammar[helper_name].append([''])
                            else:
                                grammar[helper_name].append(generation[k][len(longest):])
                        else:
                            grammar[keys[i]][j] = grammar[keys[i]][k]
                            j = j + 1
                    grammar[keys[i]] = [[*longest, helper_name]] + grammar[keys[i]][:j]

        return grammar

    @staticmethod
    def remove_left_recursion(grammar: dict):
        keys = list(grammar.keys())
        for i in range(len(keys)):
            for j in range(i):
                extended = []
                for k in range(len(grammar[keys[i]])):
                    if len(grammar[keys[i]][k]) > 0 and grammar[keys[i]][k][0] == keys[j]:
                        for l in range(len(grammar[keys[j]])):
                            extended.append(grammar[keys[j]][l] + grammar[keys[i]][k][1:])
                    elif len(grammar[keys[i]][k]) > 0:
                        extended.append(grammar[keys[i]][k])
                grammar[keys[i]] = extended
            has_direct_rec = False
            for k in range(len(grammar[keys[i]])):
                if len(grammar[keys[i]][k]) > 0 and grammar[keys[i]][k][0] == keys[i]:
                    has_direct_rec = True
                    break
            if has_direct_rec:
                helper_name = keys[i] + "'"
                while helper_name in grammar:
                    helper_name = helper_name + "'"
                grammar[helper_name] = []
                j = 0
                for k in range(len(grammar[keys[i]])):
                    if len(grammar[keys[i]][k]) > 0:
                        if grammar[keys[i]][k][0] == keys[i]:
                            grammar[helper_name].append(grammar[keys[i]][k][1:] + [helper_name])
                        else:
                            if len(grammar[keys[i]][k]) == 1 and grammar[keys[i]][k][0] == '':
                                grammar[keys[i]][k] = [helper_name]
                            else:
                                grammar[keys[i]][k].append(helper_name)
                            grammar[keys[i]][j] = grammar[keys[i]][k]
                            j = j + 1
                grammar[keys[i]] = grammar[keys[i]][:j]
                grammar[helper_name].append([''])

        return grammar

    def print_grammar(self):
        print("==== PARSED LL GRAMMAR ====")
        for k, kv in self.grammar.items():
            for i in range(len(kv)):
                for j in range(len(kv[i])):
                    if kv[i][j] in ['{', '}', '(', ')', ';', '+', '*', '<', '=']:
                        kv[i][j] = '\"' + kv[i][j] + '\"'
            print(f"{k:<10} ::= ", end='')
            if len(kv) == 1:
                print(' '.join(kv[0]) + ' ;')
            else:
                for i, iv in enumerate(kv):
                    rule = ' '.join(iv)
                    if i == 0:
                        print(rule)
                    elif i == len(kv) - 1:
                        print(' ' * 13 + f"| {rule} ;")
                    else:
                        print(' ' * 13 + f"| {rule}")
        print()

    def get_terminals(self):
        terminal = []
        for v in self.grammar.values():
            if len(v) == 1:
                for i in v[0]:
                    if i not in self.nonterminals:
                        terminal.append(i)
            else:
                for i in range(len(v)):
                    for j in v[i]:
                        if j not in self.nonterminals:
                            terminal.append(j)
        return list(set(terminal))

    def find_first(self):
        first = {}
        for k in self.nonterminals:
            first[k] = set(self.calc_first(k))
        return first

    def calc_first(self, k):
        first = []
        if len(self.grammar[k]) == 1:
            value = self.grammar[k][0]
            if value[0] in self.terminals:
                first.append(value[0])
            else:
                first.extend(self.calc_first(value[0]))
        else:
            for i in range(len(self.grammar[k])):
                value = self.grammar[k][i][0]
                if value in self.terminals:
                    first.append(value)
                else:
                    first.extend(self.calc_first(value))
        return first

    def find_follow(self):
        follow = {}
        for k in self.nonterminals:
            follow[k] = set(self.calc_follow(k))
        return follow

    def calc_follow(self, target_key):
        follow = []
        if target_key == 'prog':
            follow.append('$')

        for key, value in self.grammar.items():
            if len(value) == 1:
                if target_key in value[0]:
                    index = value[0].index(target_key)
                    # not the last position
                    if index != len(value[0]) - 1:
                        if value[0][index + 1] in self.terminals:
                            follow.append(value[0][index + 1])
                        else:
                            temp_first = self.first[value[0][index + 1]].copy()
                            if '' not in temp_first:
                                follow.extend(temp_first)
                            else:
                                temp_first.remove('')
                                follow.extend(temp_first)
                                follow.extend(self.calc_follow(key))
                    # the last position
                    else:
                        if target_key != key:
                            follow.extend(self.calc_follow(key))
                        else:
                            continue
                else:
                    continue
            else:
                for i in range(len(value)):
                    if target_key in value[i]:
                        index = value[i].index(target_key)
                        # not the last position
                        if index != len(value[i]) - 1:
                            if value[i][index + 1] in self.terminals:
                                follow.append(value[i][index + 1])
                            else:
                                temp_first = self.first[value[i][index + 1]].copy()
                                if '' not in temp_first:
                                    follow.extend(temp_first)
                                else:
                                    temp_first.remove('')
                                    follow.extend(temp_first)
                                    follow.extend(self.calc_follow(key))
                        # the last position
                        else:
                            if target_key != key:
                                follow.extend(self.calc_follow(key))
                            else:
                                continue
                    else:
                        continue
        return follow

    def print_first_follow(self):
        print("==== FIRST & FOLLOW ====")
        print(f"{'Symbol':<10} | {'First':<30} | {'Follow':<30}")
        print(f"{'-' * 10} | {'-' * 30} | {'-' * 30}")
        for k in self.nonterminals:
            first = sorted(list(self.first[k]))
            for i in range(len(first)):
                if first[i] == '':
                    first[i] = 'ϵ'
            follow = sorted(list(self.follow[k]))
            print(f"{k:<10} | {', '.join(first):<30} | {', '.join(follow):<30}")
        print()
