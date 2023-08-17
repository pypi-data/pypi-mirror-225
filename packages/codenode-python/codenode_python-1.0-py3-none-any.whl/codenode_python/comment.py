import codenode


class Comment:
    """
    Nodes representing a python comment.
    """
    def __init__(self, content=''):
        """
        :param content: Comment content. Will be split into individual
                        lines.
        """
        self.content = content
        """
        Comment content.
        """

    def __iter__(self):
        for content in self.content.splitlines():
            yield codenode.line(f'# {content}')


def commented(node, dumps=lambda node: codenode.dumps(node)) -> Comment:
    """
    Returns a comment node whose content is based on the string output
    of processing another node.

    :param node: Node whose string output will be used as the content
                 of the comment.
    :param dumps: Function used to convert the node to a string.
    :return: New comment node.
    """
    return Comment(dumps(node))
