"""Expand Reduce Flow class."""
from typing import Sequence

from uniflow.flow.flow import Flow
from uniflow.node import Node
from uniflow.op.basic.expand_op import ExpandOp
from uniflow.op.basic.reduce_op import ReduceOp


class ExpandReduceFlow(Flow):
    """Expand Reduce Flow class."""

    def __init__(self, expand_split_function=None, reduce_merge_function=None) -> None:
        """Initialize ExpandReduceFlow class."""
        super().__init__()
        self.expand_op = ExpandOp(split_function=expand_split_function)
        self.reduce_op = ReduceOp(merge_function=reduce_merge_function)

    def run(self, nodes: Sequence[Node]) -> Sequence[Node]:
        """Run the ExpandReduce flow.

        Args:
            nodes (Sequence[Node]): Input nodes.

        Returns:
            Sequence[Node]: Output nodes.
        """
        # Apply the Expand operation
        expanded_nodes = self.expand_op(nodes)

        # Apply the Reduce operation
        reduced_node = self.reduce_op(expanded_nodes)

        return reduced_node
