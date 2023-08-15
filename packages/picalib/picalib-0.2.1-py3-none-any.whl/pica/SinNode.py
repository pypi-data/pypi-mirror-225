import math

class SinNode:
    def __init__(self, node):
        self.value = node.result
        self.result = math.sin(math.radians(self.value))
        self.gradient = 0
        self.children = [node]
        self.parents = []
        node.parents.append(self)
  
