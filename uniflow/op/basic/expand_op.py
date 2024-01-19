"""Expand operation."""
import copy
from typing import Any, Mapping, Sequence, Callable, Tuple

from uniflow.node import Node
from uniflow.op.op import Op


class ExpandOp(Op):
    """Expand operation class."""

    def __init__(self, split_function: Callable[[Mapping[str, Any]], Tuple[Mapping[str, Any], Mapping[str, Any]]] = None):
        """
        Initialize ExpandOp with an optional split function.

        Args:
            split_function (Callable[[Mapping[str, Any]], (Mapping[str, Any], Mapping[str, Any])]): Function to split the value dict.
        """
        super().__init__(name="ExpandOp")
        self.split_function = split_function if split_function else self.default_split_function

    @staticmethod
    def default_split_function(value_dict: Mapping[str, Any]) -> (Mapping[str, Any], Mapping[str, Any]):
        """
        Default function to split the value dict into two halves.

        Args:
            value_dict (Mapping[str, Any]): Input value dict.

        Returns:
            Tuple[Mapping[str, Any], Mapping[str, Any]]: Two output value dicts.
        """
        n = len(value_dict)
        first_half = dict(list(value_dict.items())[:n//2])
        second_half = dict(list(value_dict.items())[n//2:])
        return first_half, second_half

    def __call__(self, nodes: Sequence[Node]) -> Sequence[Node]:
        """Call expand operation.

        Args:
            nodes (Sequence[Node]): Input nodes.

        Returns:
            Sequence[Node]: Output nodes.
        """
        output_nodes = []
        for node in nodes:
            first_half, second_half = self.split_function(node.value_dict)
            output_nodes.append(
                Node(name=self.unique_name(), value_dict=first_half, prev_nodes=[node])
            )
            output_nodes.append(
                Node(name=self.unique_name(), value_dict=second_half, prev_nodes=[node])
            )
        return output_nodes
