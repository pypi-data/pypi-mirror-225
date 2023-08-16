class ExpNode:
    def __init__(self, node1,node2):
        self.value = node1.result
        self.coefficient = node2.result
        self.result = node2.result ** self.value
        self.gradient = 0
        self.children = [node1,node2]
        self.parents = []
        node1.parents.append(self)
        node2.parents.append(self)
  