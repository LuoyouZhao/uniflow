"""Reduce operation."""
from typing import Any, Mapping, Sequence, Callable

from uniflow.node import Node
from uniflow.op.op import Op


class ReduceOp(Op):
    """Reduce operation class."""

    def __init__(self, merge_function: Callable[[Mapping[str, Any], Mapping[str, Any]], Mapping[str, Any]] = None):
        """
        Initialize ReduceOp with an optional merge function.

        Args:
            merge_function (Callable[[Mapping[str, Any], Mapping[str, Any]], Mapping[str, Any]]): Function to merge two value dicts.
        """
        super().__init__(name="ReduceOp")
        self.merge_function = merge_function if merge_function else self.default_merge_function

    @staticmethod
    def default_merge_function(value_dict1: Mapping[str, Any], value_dict2: Mapping[str, Any]) -> Mapping[str, Any]:
        """
        Default function to merge two value dicts.

        Args:
            value_dict1 (Mapping[str, Any]): First input value dict.
            value_dict2 (Mapping[str, Any]): Second input value dict.

        Returns:
            Mapping[str, Any]: Merged output value dict.
        """
        merged_dict = {}
        for key1, value1 in value_dict1.items():
            for key2, value2 in value_dict2.items():
                merged_key = f"{key1} {key2}"
                merged_value = (value1, value2)
                merged_dict[merged_key] = merged_value
        return merged_dict

    def __call__(self, nodes: Sequence[Node]) -> Sequence[Node]:
        """Call reduce operation.

        Args:
            nodes (Sequence[Node]): Input nodes (expecting two nodes: expand_1 and expand_2).

        Returns:
            Sequence[Node]: Output node (reduce_1).
        """
        if len(nodes) != 2:
            raise ValueError("ReduceOp expects exactly two input nodes.")

        merged_value_dict = self.merge_function(nodes[0].value_dict, nodes[1].value_dict)
        output_node = Node(name=self.unique_name(), value_dict=merged_value_dict, prev_nodes=nodes)
        return [output_node]
