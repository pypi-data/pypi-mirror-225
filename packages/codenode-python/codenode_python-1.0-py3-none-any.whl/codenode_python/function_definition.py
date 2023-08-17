from codenode import line
from typing import Optional

from .node import Node


class Function(Node):
    """
    Nodes representing a python function definition.
    """

    def __init__(self, name: str, *args: str, **kwargs: str):
        """
        :param name: Name of function.
        :param args: Positional argument names of function.
        :param kwargs: Keyword argument names and values of function.
        """
        super().__init__()
        self.name: str = name
        """
        Name of function.
        """

        self.args: 'tuple[str]' = args
        """
        Tuple of positional argument names of function.
        """

        self.kwargs: 'dict[str, str]' = kwargs
        """
        Keyword argument names and values of function.
        """

        self.decorators: 'list[str]' = []
        """
        List of decorators applied to this function definition, 
        each one a single string.
        """

        self.return_type: Optional[str] = None
        """
        Return type annotation of function.
        """

    def add_decorator(self, decorator: str):
        """
        Adds a decorator to this function definition.

        :param decorator: Decorator to add.
        """
        self.decorators.append(decorator)

    def header(self):
        for decorator in self.decorators:
            yield line(f'@{decorator}')

        arg_string = ', '.join(self.args)
        if self.kwargs:
            if self.args:
                arg_string += ', '

            arg_string += ', '.join(
                f'{key}={value}' for key, value in self.kwargs.items()
            )

        yield line(
            f'def {self.name}({arg_string})'
            f'{f" -> {self.return_type}" if self.return_type is not None else ""}'
            f':'
        )

