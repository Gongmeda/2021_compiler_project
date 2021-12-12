class Node:
    def __init__(self, key, parent, index, value=None):
        self.key = key
        self.parent = parent
        self.children = []
        self.index = index
        self.value = value

    def add_child(self, keys):
        for idx, item in enumerate(keys):
            node = Node(item, self, idx)
            self.children.append(node)
        return self.children[0]

    def advance(self):
        node = self
        while True:
            if node.parent is not None:
                if len(node.parent.children) - 1 == node.index:
                    node = node.parent
                else:
                    break
            else:
                return node
        cur = node.parent.children[node.index + 1]
        while len(cur.children) != 0:
            cur = cur.children[0]
        return cur

    def get_root(self):
        node = self
        while node.parent is not None:
            node = node.parent
        return node

    @staticmethod
    # Reference - https://stackoverflow.com/questions/30893895/how-to-print-a-tree-in-python
    def print_tree(current_node, indent="", last='updown'):
        nb_children = lambda node: node.index
        size_branch = {child: nb_children(child) for child in current_node.children}

        """ Creation of balanced lists for "up" branch and "down" branch. """
        up = sorted(current_node.children, key=lambda node: nb_children(node))
        down = []
        while up and sum(size_branch[node] for node in down) < sum(size_branch[node] for node in up):
            down.append(up.pop())

        """ Printing of "up" branch. """
        for child in up:
            next_last = 'up' if up.index(child) == 0 else ''
            next_indent = '{0}{1}{2}'.format(indent, ' ' if 'up' in last else '│', " " * len(current_node.key))
            Node.print_tree(child, indent=next_indent, last=next_last)

        """ Printing of current node. """
        if last == 'up':
            start_shape = '┌'
        elif last == 'down':
            start_shape = '└'
        elif last == 'updown':
            start_shape = ' '
        else:
            start_shape = '├'

        if up:
            end_shape = '┤'
        elif down:
            end_shape = '┐'
        else:
            end_shape = ''

        text = current_node.key if current_node.key != '' else 'ϵ'
        if current_node.value:
            text = f"\"{current_node.value}\""
        print('{0}{1}{2}{3}'.format(indent, start_shape, text, end_shape))

        """ Printing of "down" branch. """
        for child in down:
            next_last = 'down' if down.index(child) is len(down) - 1 else ''
            next_indent = '{0}{1}{2}'.format(indent, ' ' if 'down' in last else '│', " " * len(current_node.key))
            Node.print_tree(child, indent=next_indent, last=next_last)

    def get_symbol_table(self):
        node = self.get_root()
        scope = ["global"]
        symbol_table = []
        while node.children:
            node = node.children[0]
        symbol_table.append([node.value, "function", scope[:]])
        scope.append(node.value)
        node = node.advance()

        while node.parent is not None:
            if node.key in ["char", "int"]:
                node_type = node.key
                node = node.advance()
                if node.key == "([a-z] | [A-Z])*":
                    symbol_table.append([node.value, node_type, list(scope)])
                    node = node.advance()
                    continue
            elif node.key in ["IF", "ELSE"]:
                scope.append(node.key)
            elif node.key == "}":
                scope.pop()
            node = node.advance()
        return symbol_table

    def search_inorder(self):
        node = self
        if node.children:
            return node.children[0]
        while node.parent is not None:
            if node.index != len(node.parent.children) - 1:
                return node.parent.children[node.index + 1]
            node = node.parent
        return None
