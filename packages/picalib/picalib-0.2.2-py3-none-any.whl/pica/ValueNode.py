class ValueNode:
    def __init__(self, value:int):
        self.result = value
        self.gradient = 0
        self.children = []
        self.parents = []
