import sys


class Semantic:
    def __init__(self, ast, symbol_table):
        self.ast = ast
        self.symbol_table = symbol_table
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
        return []

    def print_ir(self):
        print("==== INTERMEDIATE REPRESENTATION ====")

