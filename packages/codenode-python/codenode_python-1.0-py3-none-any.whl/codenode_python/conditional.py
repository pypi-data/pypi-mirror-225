from codenode import line
from typing import Optional

from .node import Node


class If(Node):
    """
    Nodes representing a python if statement.
    """
    def __init__(self, condition: str):
        """
        :param condition: Condition checked for by the if.
        """
        super().__init__()
        self.condition: str = condition
        """
        Condition checked for by the if.
        """

        self.elif_nodes: 'list[Elif]' = []
        """
        List of Elif nodes following the if check.
        """
        self.else_node: Optional[Else] = None
        """
        Optional Else node following the if check and its elifs.
        """

    def header(self):
        yield line(f'if {self.condition}:')

    def add_elif(self, condition: str) -> 'Elif':
        """
        Create an Elif node, add it to this node's elifs,
        then return it.

        :param condition: Condition checked for by elif.
        :return: New Elif node.
        """
        elif_node = Elif(condition)
        self.elif_nodes.append(elif_node)
        return elif_node

    def add_else(self) -> 'Else':
        """
        Create an Else node, set it to this node's else node,
        then return it.

        :return: New Else node
        """
        self.else_node = Else()
        return self.else_node

    def footer(self):
        yield self.elif_nodes

        if self.else_node:
            yield self.else_node


class Elif(Node):
    """
    Nodes representing a python elif statement.
    Don't instantiate these directly, use If.add_elif instead.
    """

    def __init__(self, condition: str):
        """

        :param condition: Condition check for by elif.
        """
        super().__init__()
        self.condition: str = condition
        """
        Condition checked for by elif.
        """

    def header(self):
        yield line(f'elif {self.condition}:')


class Else(Node):
    """
    Nodes representing a python else statement.
    Don't instantiate these directly, use the parent node's add_else
    method instead.
    """

    def header(self):
        yield line('else:')
