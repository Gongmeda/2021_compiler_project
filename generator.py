class Generator:
    def __init__(self, ir):
        self.ir = ir
        self.reg_cnt = 1
        self.prefix = 2
        self.width = 10
        self.code = self.generate()

    def generate(self):
        code = []
        for c in self.ir:
            if c[1] is None:
                if c[0][:4] == "goto":  # Jump
                    code.append(
                        f"{' ' * self.prefix}{'JUMP':<{self.width}} {' ' * self.width} {c[0][5:]:<{self.width}}")
                else:  # Label
                    code.append(c[0])
            else:
                if c[1]:
                    bt = c[1].get_bt()
                    bt.value = 1
                    self.count_register(bt)
                    code.extend(self.w_code(c[0], bt))
        return code

    def w_code(self, ir, node):
        code = []
        nid = f"Reg#{node.value}"

        if node.children:
            left = node.children[0]
            right = node.children[1]
            lid = f"Reg#{left.value}"
            rid = f"Reg#{right.value}"
            if not left.children:
                if node.key != "=":
                    code.extend(self.w_code("", left))
                code.extend(self.w_code("", right))

                if node.key == "+":
                    code.append(
                        f"{' ' * self.prefix}{'ADD':<{self.width}} {nid:<{self.width}} {lid:<{self.width}} {rid:<{self.width}}")
                elif node.key == "*":
                    code.append(
                        f"{' ' * self.prefix}{'MUL':<{self.width}} {nid:<{self.width}} {lid:<{self.width}} {rid:<{self.width}}")
                elif node.key == "=":
                    code.append(
                        f"{' ' * self.prefix}{'ST':<{self.width}} {rid:<{self.width}} {left.key:<{self.width}}")
                else:
                    code.append(
                        f"{' ' * self.prefix}{'LT':<{self.width}} {nid:<{self.width}} {lid:<{self.width}} {rid:<{self.width}}")
                    code.append("  JUMPT {},   {}".format(nid, ir.split("goto")[-1][1:]))
                    code.append(
                        f"{' ' * self.prefix}{'JUMPT':<{self.width}} {nid:<{self.width}} {ir.split('goto')[-1][1:]:<{self.width}}")
            elif not right.children:
                code.extend(self.w_code("", left))
                if node.key == "+":
                    code.append(
                        f"{' ' * self.prefix}{'ADD':<{self.width}} {nid:<{self.width}} {lid:<{self.width}} {rid:<{self.width}}")
                elif node.key == "*":
                    code.append(
                        f"{' ' * self.prefix}{'MUL':<{self.width}} {nid:<{self.width}} {lid:<{self.width}} {rid:<{self.width}}")
                elif node.key == "=":
                    code.append(
                        f"{' ' * self.prefix}{'ST':<{self.width}} {rid:<{self.width}} {left.key:<{self.width}}")
                else:
                    code.append(
                        f"{' ' * self.prefix}{'LT':<{self.width}} {nid:<{self.width}} {rid:<{self.width}} {lid:<{self.width}}")
                    code.append(
                        f"{' ' * self.prefix}{'JUMPT':<{self.width}} {nid:<{self.width}} {ir.split('goto')[-1][1:]:<{self.width}}")

            else:
                code.extend(self.w_code("", left))
                code.extend(self.w_code("", right))
                if node.key == "+":
                    code.append(
                        f"{' ' * self.prefix}{'ADD':<{self.width}} {nid:<{self.width}} {lid:<{self.width}} {rid:<{self.width}}")
                elif node.key == "*":
                    code.append(
                        f"{' ' * self.prefix}{'MUL':<{self.width}} {nid:<{self.width}} {lid:<{self.width}} {rid:<{self.width}}")
                elif node.key == "=":
                    code.append(
                        f"{' ' * self.prefix}{'ST':<{self.width}} {rid:<{self.width}} {left.key:<{self.width}}")
                else:
                    code.append(
                        f"{' ' * self.prefix}{'LT':<{self.width}} {nid:<{self.width}} {lid:<{self.width}} {rid:<{self.width}}")
                    code.append(
                        f"{' ' * self.prefix}{'JUMPT':<{self.width}} {nid:<{self.width}} {ir.split('goto')[-1][1:]:<{self.width}}")
        elif ir[:4] == "EXIT":
            code.append(
                f"{' ' * self.prefix}{'LD':<{self.width}} {'rax':<{self.width}} {'-1':<{self.width}}")
        elif str(node.value).isdigit():
            code.append(
                f"{' ' * self.prefix}{'LD':<{self.width}} {'Reg#'+str(node.value):<{self.width}} {node.key:<{self.width}}")
        return code

    def count_register(self, node):
        if node.children:
            left = node.children[0]
            right = node.children[1]
            if node.key == "=":
                right.value = node.value
                self.count_register(right)
            elif not right.children:
                left.value = node.value
                right.value = node.value + 1
                self.reg_cnt = max(self.reg_cnt, right.value)
                self.count_register(left)
            elif not left.children:
                left.value = node.value + 1
                right.value = node.value
                self.reg_cnt = max(self.reg_cnt, left.value)
                self.count_register(right)
            else:
                left.value = node.value
                right.value = node.value + 1
                self.reg_cnt = max(self.reg_cnt, right.value)
                self.count_register(left)
                self.count_register(right)

    def write_code(self, file):
        for c in self.code:
            file.write(f"{c}\n")
        file.write(f"\nUsed Register Count: {self.reg_cnt}")
        file.close()
