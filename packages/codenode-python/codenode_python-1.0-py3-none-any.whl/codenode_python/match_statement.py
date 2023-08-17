from codenode import line, indent, dedent
from .node import Node


class Case(Node):
    """
    Nodes representing a case block in a python match statement.
    Don't instantiate these directly, use the parent node's add_case
    method instead.
    """
    def __init__(self, pattern: str):
        """
        :param pattern: Pattern this case will match to.
        """
        super().__init__()
        self.pattern: str = pattern
        """
        Pattern this case will match to.
        """

    def header(self):
        yield line(f'case {self.pattern}:')


class Match:
    """
    Nodes representing a python match statement.
    """
    def __init__(self, subject: str):
        """
        :param subject: Subject of match statement.
        """
        self.subject: str = subject
        """
        Subject of match statement.
        """
        self.cases: 'list[Case]' = list()
        """
        List of case block nodes belonging to this match statement.
        """

    def __iter__(self):
        yield line(f'match {self.subject}:')
        yield indent
        yield from self.cases
        yield dedent

    def add_case(self, pattern: str) -> Case:
        """
        Creates a new case node, adds it to this node's case node list,
        then returns it.

        :param pattern: Pattern new case will match to.
        :return: New case node.
        """
        case_node = Case(pattern)
        self.cases.append(case_node)
        return case_node
