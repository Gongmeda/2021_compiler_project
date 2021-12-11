import sys


# LL(1) Parser
class LLParser:
    def __init__(self, tokens, grammar_path):
        self.tokens = tokens
        self.grammar = self.parse_grammar(grammar_path)
        self.nonterminals = list(self.grammar.keys())
        self.terminals = self.get_terminals()
        self.nullable = self.find_nullable()
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

    def find_nullable(self):
        keys = self.nonterminals
        grammar = self.grammar
        nullable = {}
        for i in range(len(keys)):
            for j in range(len(grammar[keys[i]])):
                for k in range(len(grammar[keys[i]][j])):
                    if grammar[keys[i]][j][k] not in grammar:
                        nullable[grammar[keys[i]][j][k]] = False
        if '' in nullable:
            nullable[''] = True

        def calc_rec(key, path: list):
            nonlocal nullable

            if key in path:
                return False
            path.append(key)
            if key in nullable:
                return nullable[key]
            for ii in range(len(grammar[key])):
                jj = 0
                while jj < len(grammar[key][ii]):
                    if not calc_rec(grammar[key][ii][jj], path[:]):
                        break
                    jj = jj + 1
                if jj == len(grammar[key][ii]):
                    nullable[key] = True
                    return True
            nullable[key] = False
            return False

        for k in keys:
            calc_rec(k, [])
        return nullable

    def find_first(self):
        keys = self.nonterminals
        grammar = self.grammar
        nullable = self.nullable
        finished = False
        first = {}
        for i in range(len(keys)):
            for j in range(len(grammar[keys[i]])):
                for k in range(len(grammar[keys[i]][j])):
                    if grammar[keys[i]][j][k] not in grammar:
                        first[grammar[keys[i]][j][k]] = [grammar[keys[i]][j][k]]

        def calc_rec(key, path: list):
            nonlocal finished

            if key not in grammar:
                return first[key]
            if key in path:
                return first[key]
            path.append(key)
            if key not in first:
                first[key] = []
                finished = False
            for ii in range(len(grammar[key])):
                jj = 0
                while jj < len(grammar[key][ii]):
                    f = calc_rec(grammar[key][ii][jj], path[:])
                    for kk in range(len(f)):
                        if f[kk] not in first[key] and f[kk] != '':
                            first[key].append(f[kk])
                            finished = False
                    if not nullable[grammar[key][ii][jj]]:
                        break
                    jj = jj + 1
                if jj == len(grammar[key][ii]):
                    if '' not in first[key]:
                        first[key].append('')
            return first[key]

        while not finished:
            finished = True
            for i in range(len(keys)):
                calc_rec(keys[i], [])
        for k in first.keys():
            first[k].sort()
        return first

    def find_follow(self):
        keys = self.nonterminals
        grammar = self.grammar
        nullable = self.nullable
        first = self.first
        finished = False
        follow = {}
        for i in range(len(keys)):
            if i == 0:
                follow[keys[i]] = ['$']
            else:
                follow[keys[i]] = []

        def calc(key):
            nonlocal finished

            for ii in range(len(grammar[key])):
                for jj in range(len(grammar[key][ii])):
                    mid = grammar[key][ii][jj]
                    if mid in grammar:
                        kk = jj + 1
                        while kk < len(grammar[key][ii]):
                            f = first[grammar[key][ii][kk]]
                            for ll in range(len(f)):
                                if f[ll] != '' and f[ll] not in follow[mid]:
                                    follow[mid].append(f[ll])
                                    finished = False
                            if not nullable[grammar[key][ii][kk]]:
                                break
                            kk = kk + 1
                        if kk == len(grammar[key][ii]):
                            for ll in range(len(follow[key])):
                                if follow[key][ll] not in follow[mid]:
                                    follow[mid].append(follow[key][ll])
                                    finished = False

        while not finished:
            finished = True
            for i in range(len(keys)):
                calc(keys[i])
        for k in keys:
            follow[k].sort()
        return follow

    # def calc_follow(self, k):
    #     follow = []
    #     if k == 'prog':
    #         follow.append('$')
    #
    #     for kk, kv in self.grammar.items():
    #         for i in range(len(kv)):
    #             if k in kv[i]:
    #                 idx = kv[i].index(k)
    #                 if idx != len(kv[i]) - 1:
    #                     if kv[i][idx + 1] in self.terminals:
    #                         follow.append(kv[i][idx + 1])
    #                     else:
    #                         first = self.first[kv[i][idx + 1]].copy()
    #                         if '' not in first:
    #                             follow.extend(first)
    #                         else:
    #                             first.remove('')
    #                             follow.extend(list(first) + self.calc_follow(kk))
    #                 else:
    #                     if k != kk:
    #                         follow.extend(self.calc_follow(kk))
    #                     else:
    #                         continue
    #             else:
    #                 continue
    #     return follow

    def print_first_follow(self):
        first_len = 35
        follow_len = 35
        print("==== FIRST & FOLLOW ====")
        print(f"{'Symbol':<10} | {'Nullable':<10} | {'First':<{first_len}} | {'Follow':<{follow_len}}")
        print(f"{'-' * 10} | {'-' * 10} | {'-' * first_len} | {'-' * follow_len}")
        for k in self.nonterminals:
            first = sorted(list(self.first[k]))
            for i in range(len(first)):
                if first[i] == '':
                    first[i] = 'ϵ'
            follow = sorted(list(self.follow[k]))
            print(f"{k:<10} | {'True' if self.nullable[k] else 'False':<10} "
                  f"| {', '.join(first):<{first_len}} | {', '.join(follow):<{follow_len}}")
        print()
