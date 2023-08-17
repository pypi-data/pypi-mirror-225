from codenode import line


class Call:
    """
    Nodes representing a python function call.
    """

    def __init__(self, name: str, *args: str, **kwargs: str):
        """
        :param name: Name of function.
        :param args: Positional arguments passed to function call.
        :param kwargs: Keyword arguments passed to function call.
        """
        self.name = name
        """
        Name of arguments.
        """
        self.args: 'tuple[str]' = args
        """
        Tuple of positional arguments passed to function call.
        """
        self.kwargs: 'dict[str, str]' = kwargs
        """
        Dict of keyword arguments passed to function call.
        """

    def __iter__(self):
        arg_string = ', '.join(self.args)
        if self.kwargs:
            if self.args:
                arg_string += ', '

            arg_string += ', '.join(
                f'{key}={value}' for key, value in self.kwargs.items()
            )

        yield line(f'{self.name}({arg_string})')
