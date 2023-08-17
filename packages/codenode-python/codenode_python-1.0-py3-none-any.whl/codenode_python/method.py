from .function_definition import Function


class Method(Function):
    """
    Nodes representing a method definition.
    Don't instantiate these directly, use the parent node's add_method
    method instead.
    """
    def __init__(self, name, *args: str, **kwargs: str):
        """
        :param name: Name of method.
        :param args: Positional argument names of method.
        :param kwargs: Keyword argument names and values of method.
        """
        super().__init__(name, 'self', *args, **kwargs)
