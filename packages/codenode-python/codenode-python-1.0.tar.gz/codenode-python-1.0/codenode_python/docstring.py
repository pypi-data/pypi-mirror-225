from codenode import line


class DocString:
    """
    Nodes representing a python docstring.
    """
    def __init__(self, content=''):
        """
        :param content: Content of docstring.
                        Will be broken down into separate lines.
        """
        self.content = content
        """
        Content of docstring.
        """

    def __iter__(self):
        yield line('"""')
        yield from map(line, self.content.splitlines())
        yield line('"""')
