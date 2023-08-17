from .node import Node
from .conditional import Else
from codenode import line
from typing import Optional


class Except(Node):
    """
    Nodes representing an except block following a python try block.
    Don't instantiate these directly, use the parent method's add_except
    method instead.
    """
    def __init__(
            self,
            types=(),
            name: Optional[str] = None,
            exception_group=False
    ):
        """
        :param types: Exception types this clause catches.
        :param name: Named assigned to caught exception.
        :param exception_group: If true, exception clause is treated as
                                an exception group extraction clause
                                instead.
        """
        super().__init__()
        self.types: 'tuple[str, ...]' = types
        """
        Exception types this clause catches.
        """

        self.name: Optional[str] = name
        """
        Named assigned to caught exception.
        """

        self.exception_group: bool = exception_group
        """
        If true, exception clause is treated as an exception group 
        extraction clause instead.
        """

    def header(self):
        types_string = ''
        if self.types:
            types_string = ", ".join(self.types)
            if len(self.types) > 1:
                types_string = f'({types_string})'
            if self.name:
                types_string += f' as {self.name}'
            types_string = f' {types_string}'

        yield line(
            f'except{"*" if self.exception_group else ""}{types_string}:'
        )


class Finally(Node):
    """
    Node representing a finally clause following a python try statement.
    Don't instantiate these directly, use the parent node's add_finally
    method instead.
    """
    def header(self):
        yield line('finally:')


class Try(Node):
    """
    Nodes representing a python try statement.
    """
    def __init__(self):
        super().__init__()

        self.except_nodes: 'list[Except]' = list()
        """
        List of except nodes following this try statement node.
        """

        self.finally_node: Optional[Finally] = None
        """
        Optional finally clause node following this try statement node.
        """

        self.else_node: Optional[Else] = None
        """
        Optional else node following this try statement node.
        """

    def add_except(
            self,
            types: 'tuple[str, ...]' = (),
            name: Optional[str] = None,
            exception_group=False,
    ) -> Except:
        """
        Creates a new except clause node, adds it to this node's list of
        except nodes, then returns it.

        :param types: Exception types this clause catches.
        :param name: Named assigned to caught exception.
        :param exception_group: If true, exception clause is treated as
                                an exception group extraction clause
                                instead.
        :return: New except clause node.
        """
        except_node = Except(types, name, exception_group)
        self.except_nodes.append(except_node)
        return except_node

    def add_else(self) -> Else:
        """
        Creates a new else node, sets it as this node's else node,
        then returns it.

        :return: New else node.
        """
        self.else_node = Else()
        return self.else_node

    def add_finally(self) -> Finally:
        """
        Creates a new finally node, sets it as this node's finally node,
        then returns it.

        :return: New finally node.
        """
        self.finally_node = Finally()
        return self.finally_node

    def header(self):
        yield line('try:')

    def footer(self):
        yield from self.except_nodes
        if self.else_node:
            yield self.else_node
        if self.finally_node:
            yield self.finally_node

