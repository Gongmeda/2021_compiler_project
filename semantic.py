import sys
from syntax_tree import Node


class Semantic:
    def __init__(self, ast, symbol_table):
        self.ast: Node = ast
        self.symbol_table = symbol_table
        self.label_idx = 1
        self.check_semantics()
        self.ir = self.create_ir()

    def check_semantics(self):
        symbol_table = [(i[0], i[1], ' '.join(i[2])) for i in self.symbol_table]
        symbol_set = {s[0]: s[1] for s in symbol_table}
        if len(symbol_table) != len(set(symbol_table)):
            sys.exit("Semantic Error: duplicate variables declared in same scope")

        node = self.ast
        while node.children:
            node = node.children[0]
        node = node.advance()
        variable_type = ''
        while node.parent is not None:
            if node.key in ["([a-z] | [A-Z])*", "[0-9]*"]:
                if node.parent.parent.key == "stat":
                    try:
                        variable_type = symbol_set[node.value]
                    except KeyError:
                        sys.exit(f"Semantic Error: Undeclared variable \"{node.value}\"")
                elif node.parent.parent.key == "fact":
                    try:
                        value_type = symbol_set[node.value]
                    except KeyError:
                        if node.key == "[0-9]*":
                            value_type = "int"
                        else:
                            value_type = "char"
                    if value_type in ["char", "int"] and variable_type != value_type:
                        sys.exit("Semantic Error: Type mismatch")
            node = node.advance()

    def create_ir(self):
        node = self.ast.get_root()
        prog_name = node.children[0].children[0].value
        ir = [[f"BEGIN {prog_name}", None]]
        ir.extend(self.calc_ir(node))
        ir.append([f"END {prog_name}", None])
        return ir

    def calc_ir(self, node: Node):
        ir = []
        last_node = node
        while last_node.children:
            last_node = last_node.children[-1]

        while node != last_node:
            if node.key == "stat":
                n = node.children[0]
                if n.key in ["word", "EXIT"]:
                    ir.append([self.word_exit_code(n), node])
                    pass
                elif n.key == "IF":
                    ir.extend(self.if_code(node))
            node = node.search_inorder()
        return ir

    def word_exit_code(self, node):
        if node.key == "EXIT":
            r = node.key
        else:
            r = node.children[0].value
        while node.key != ";":
            node = node.advance()
            if node.value is not None:
                r += f" {node.value}"
            else:
                r += f" {node.key}"
        return r[:-2]

    def if_code(self, node):
        ir = []
        label1 = self.label_idx
        label2 = self.label_idx + 1
        self.label_idx += 2

        cond = node.children[1]
        cond_ir = node.children[1]
        then_block = node.children[3]
        else_block = node.children[5]

        then_ir = self.calc_ir(then_block)
        else_ir = self.calc_ir(else_block)

        condition = ""
        while cond.children:
            cond = cond.children[0]
        while cond.key != "{":
            if cond.value:
                condition += f" {cond.value}"
            elif cond.key:
                condition += f" {cond.key}"
            cond = cond.advance()

        ir.append([f"if{condition} goto L{label1}", cond_ir])
        ir.extend(else_ir)
        ir.append([f"goto L{label2}", None])
        ir.append([f"L{label1}", None])
        ir.extend(then_ir)
        ir.append([f"L{label2}", None])
        return ir

    def print_ir(self):
        print("==== INTERMEDIATE REPRESENTATION ====")
        for r in self.ir:
            print(f"{r[0]:<10}")
