import networkx as nx
import matplotlib.pyplot as plt
import math
from .SumNode import SumNode
from .MultNode import MultNode
from .SubNode import SubNode
from .DivNode import DivNode
from .ValueNode import ValueNode
from .SinNode import SinNode
from .CosNode import CosNode
from .TanNode import TanNode
from .CscNode import CscNode
from .SecNode import SecNode
from .CotNode import CotNode
from .LnNode import LnNode
from .LogNode import LogNode


class Graph:
    def __init__(self):
        self.graph = nx.DiGraph()

    def node(self, node):
        self.graph.add_node(node)

    def connect(self, node1, node2):
        self.graph.add_edge(node1, node2)

    def print_nodes(self):
        print(self.graph.nodes())

    def print_hello(self):
        print("Hello Autodiff")

    def draw_graph(self):
        pos = nx.circular_layout(self.graph)
        nx.draw(
            self.graph,
            pos,
            with_labels=True,
            node_size=500,
            node_color="skyblue",
            font_size=10,
            font_weight="bold",
            edge_color="gray",
        )

        plt.show()

    def forward(self):
        nodes = list(self.graph.nodes)
        return nodes[-1].result

    def backward(self):
        nodes = list(self.graph.nodes)
        nodes[-1].gradient = 1

        for node in reversed(nodes):
            if len(node.parents) > 0:
                for parent in node.parents:
                    if isinstance(parent, SumNode):
                        node.gradient += parent.gradient * 1

                    if isinstance(parent, SubNode):
                        if node == parent.children[0]:
                            node.gradient += parent.gradient * 1
                        if node == parent.children[1]:
                            node.gradient += parent.gradient * -1

                    if isinstance(parent, MultNode):
                        if node == parent.children[0]:
                            node.gradient += parent.gradient * parent.gradient1
                        if node == parent.children[1]:
                            node.gradient += parent.gradient * parent.gradient2

                    if isinstance(parent, DivNode):
                        if node == parent.children[0]:
                            node.gradient += parent.gradient * parent.gradient1
                        if node == parent.children[1]:
                            node.gradient += parent.gradient * parent.gradient2

                    if isinstance(parent, SinNode):
                        node.gradient += parent.gradient * math.cos(
                            math.radians(parent.value)
                        )

                    if isinstance(parent, CosNode):
                        node.gradient += parent.gradient * -(
                            math.sin(math.radians(parent.value))
                        )

                    if isinstance(parent, TanNode):
                        node.gradient += parent.gradient * (
                            1 / (math.cos(math.radians(parent.value)) ** 2)
                        )

                    if isinstance(parent, CscNode):
                        node.gradient += parent.gradient * (
                            -(1 / math.tan(math.radians(parent.value)))
                            * (1 / math.sin(math.radians(parent.value)))
                        )

                    if isinstance(parent, SecNode):
                        node.gradient += parent.gradient * (
                            (1 / math.cos(math.radians(parent.value)))
                            * math.tan(math.radians(parent.value))
                        )

                    if isinstance(parent, CotNode):
                        node.gradient += parent.gradient * (
                            -(1 / (math.sin(math.radians(parent.value)) ** 2))
                        )

                    if isinstance(parent, LnNode):
                        node.gradient += parent.gradient * (1 / parent.value)

                    if isinstance(parent, LogNode):
                        node.gradient += parent.gradient * (
                            1 / (parent.value * math.log(10))
                        )
