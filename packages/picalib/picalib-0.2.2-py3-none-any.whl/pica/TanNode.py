import math


class TanNode:
    def __init__(self, node):
        self.value = node.result
        self.result = math.tan(math.radians(self.value))
        self.gradient = 0
        self.children = [node]
        self.parents = []
        node.parents.append(self)
