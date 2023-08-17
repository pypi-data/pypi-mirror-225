from codenode import line

from .method import Method
from .node import Node


class Class(Node):
    """
    Nodes representing a python class definition.

    """
    def __init__(self, name, *parents):
        """
        :param name: Name of class.
        :param parents:Parent class names/
        """
        super().__init__()

        self.name: str = name
        """
        Name of class.
        """
        self.parents: 'tuple[str]' = parents
        """
        Tuple of parent class names.
        """

        self.decorators: 'list[str]' = list()
        """
        List of decorators applied to this class definition, each one a 
        single string.
        """

    def add_decorator(self, decorator: str):
        """
        Adds a decorator to this class definition.

        :param decorator: Decorator to add.
        """
        self.decorators.append(decorator)

    def header(self):
        for decorator in self.decorators:
            yield line(f'@{decorator}')
        if self.parents:
            yield line(f"class {self.name}({', '.join(self.parents)}):")
        else:
            yield line(f'class {self.name}:')

    def add_method(self, name: str, *args: str, **kwargs: str) -> Method:
        """
        Creates a method definition, adds it to this class definition's
        body, then returns it.

        :param name: Name of method.
        :param args: Positional argument names of method.
        :param kwargs: Keyword argument names and values of method.
        :return: New method.
        """
        return self.add_child(Method(name, *args, **kwargs))
