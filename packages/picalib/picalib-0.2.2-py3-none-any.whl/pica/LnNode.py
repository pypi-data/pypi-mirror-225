import math

class LnNode:
    def __init__(self, node):
        self.value = node.result
        self.result = math.log(self.value)
        self.gradient = 0
        self.children = [node]
        self.parents = []
        node.parents.append(self)
  
