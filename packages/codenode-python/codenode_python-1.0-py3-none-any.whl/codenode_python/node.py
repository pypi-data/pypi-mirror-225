from codenode import line
import codenode_utilities


class Node(codenode_utilities.PartitionedNode):
    """
    Nodes that can contain an arbitrary number of
    inner python statements.

    Due to inheriting from PartitionedNode:
    - Each node has a list of children nodes, along with a
      add_child and add_children method
    - Each node has an inherited convenience dump/dumps method.
    - Overridable methods yielding nodes for three different innner
      sections:
        - header
        - body (indented by default in `PartitionedNode.__iter__`)
        - footer

    Documentation for ParitionedNode can be viewed
    [here](https://github.com/0xf0f/codenode/tree/master/codenode_utilities#codenode_utilitiespartitionednode).


    Will output a single 'pass' line as its body section if no other
    nodes are added as its children.
    """
    def body(self):
        if self.children:
            yield from self.children
        else:
            yield from line('pass')
