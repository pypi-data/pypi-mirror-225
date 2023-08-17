from codenode import line
from typing import Optional

from .conditional import Else
from .node import Node


class While(Node):
    """
    Nodes representing a python while loop statement.
    """
    def __init__(self, condition: str):
        """
        :param condition: The condition the while loop will check.
        """
        super().__init__()

        self.condition = condition
        """
        The condition the while loop will check.
        """

        self.else_node: Optional[Else] = None
        """
        Optional else node following this while statement node.
        """

    def header(self):
        yield line(f'while {self.condition}:')

    def footer(self):
        if self.else_node:
            yield self.else_node

    def add_else(self):
        """
        Creates a new else node, sets it as this node's else node,
        then returns it.

        :return: New else node.
        """
        self.else_node = Else()
        return self.else_node
