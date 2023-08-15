class DivNode:
    def __init__(self, node1, node2: int):
        self.value = node1.result
        self.value2 = node2.result
        self.result = self.value / self.value2
        self.gradient = 0
        self.gradient1 = 1/self.value2
        self.gradient2 = -(self.value/(self.value2**2))
        self.children = [node1,node2]
        self.parents = []
        node1.parents.append(self)
        node2.parents.append(self)

   