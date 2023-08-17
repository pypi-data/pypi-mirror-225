from codenode import line
from .node import Node


class With(Node):
    """
    Nodes representing a python with statement.
    """

    def __init__(self, *expressions: str):
        """
        :param expressions: Expressions used within the context of the
                            with block.
        """
        super().__init__()

        self.expressions: 'tuple[str]' = expressions
        """
        Expressions used within the context of the with block.
        """

    def header(self):
        yield line(f'with {",".join(self.expressions)}:')
