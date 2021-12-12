class Node:
    def __init__(self, value, parent, index):
        self.value = value
        self.parent = parent
        self.children = []
        self.index = index

    def add_child(self, values):
        for idx, item in enumerate(values):
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
            next_indent = '{0}{1}{2}'.format(indent, ' ' if 'up' in last else '│', " " * len(current_node.value))
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

        print('{0}{1}{2}{3}'.format(indent, start_shape, current_node.value if current_node.value != '' else 'ϵ', end_shape))

        """ Printing of "down" branch. """
        for child in down:
            next_last = 'down' if down.index(child) is len(down) - 1 else ''
            next_indent = '{0}{1}{2}'.format(indent, ' ' if 'down' in last else '│', " " * len(current_node.value))
            Node.print_tree(child, indent=next_indent, last=next_last)
