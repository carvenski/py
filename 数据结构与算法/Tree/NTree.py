"""
Tree with N children
"""

class NTreeNode(object):
    def __init__(self, value, children):
        self.value = value
        self.children = children # children is list

    def iter(self):
        print(self.value)
        for node in self.children:
            iter(node)



