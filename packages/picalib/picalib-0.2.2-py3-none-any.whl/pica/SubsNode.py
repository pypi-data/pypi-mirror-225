class SubsNode:
    def __init__(self, node1, node2: int):
        self.value = node1.result
        self.value2 = node2.result
        self.result = self.value - self.value2
        self.gradient = 1
        self.children = [node1,node2]

   