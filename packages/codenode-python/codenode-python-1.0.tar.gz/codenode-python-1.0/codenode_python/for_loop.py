from codenode import line
from .node import Node
from .conditional import Else


class For(Node):
    """
    Nodes representing a python for loop.
    """
    def __init__(self, expression: str):
        """
        :param expression: Expression iterated over by the for loop.
        """
        super().__init__()

        self.expression: str = expression
        """
        Expression iterated over by the for loop.
        """

        self.else_node: Else = None
        """
        Optional Else node following the for loop.
        """

    def header(self):
        yield line(f'for {self.expression}:')

    def footer(self):
        if self.else_node:
            yield self.else_node

    def add_else(self) -> Else:
        """
        Create an Else node, set it to this node's else node,
        then return it.

        :return: New Else node
        """
        self.else_node = Else()
        return self.else_node
