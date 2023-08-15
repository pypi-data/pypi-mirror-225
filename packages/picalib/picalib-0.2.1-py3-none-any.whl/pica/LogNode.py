import math

class LogNode:
    def __init__(self, node):
        self.value = node.result
        self.result = math.log(self.value,10)
        self.gradient = 0
        self.children = [node]
        self.parents = []
        node.parents.append(self)
  
