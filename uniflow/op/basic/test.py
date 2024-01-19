import unittest
from expand_op import ExpandOp
from reduce_op import ReduceOp
from uniflow.node import Node

class TestExpandOp(unittest.TestCase):
    def test_expand_op_even_elements(self):
        value_dict = {"1": "a", "2": "b", "3": "c", "4": "d"}
        root_node = Node(name="root", value_dict=value_dict)
        expand_op = ExpandOp()
        expanded_nodes = expand_op([root_node])
        self.assertEqual(len(expanded_nodes), 2)
        self.assertEqual(expanded_nodes[0].value_dict, {"1": "a", "2": "b"})
        self.assertEqual(expanded_nodes[1].value_dict, {"3": "c", "4": "d"})

    def test_expand_op_odd_elements(self):
        value_dict = {"1": "a", "2": "b", "3": "c"}
        root_node = Node(name="root", value_dict=value_dict)
        expand_op = ExpandOp()
        expanded_nodes = expand_op([root_node])
        self.assertEqual(len(expanded_nodes), 2)
        self.assertEqual(expanded_nodes[0].value_dict, {"1": "a"})
        self.assertEqual(expanded_nodes[1].value_dict, {"2": "b", "3": "c"})

    def test_expand_op_single_element(self):
        value_dict = {"1": "a"}
        root_node = Node(name="root", value_dict=value_dict)
        expand_op = ExpandOp()
        expanded_nodes = expand_op([root_node])
        self.assertEqual(len(expanded_nodes), 2)
        self.assertEqual(expanded_nodes[1].value_dict, {"1": "a"})
        self.assertEqual(expanded_nodes[0].value_dict, {})

    def test_expand_op_empty_dict(self):
        value_dict = {}
        root_node = Node(name="root", value_dict=value_dict)
        expand_op = ExpandOp()
        expanded_nodes = expand_op([root_node])
        self.assertEqual(len(expanded_nodes), 2)
        self.assertEqual(expanded_nodes[0].value_dict, {})
        self.assertEqual(expanded_nodes[1].value_dict, {})


class TestReduceOp(unittest.TestCase):
    def test_reduce_op_non_empty_dicts(self):
        expand_1 = Node(name="expand_1", value_dict={"1": "a", "2": "b"})
        expand_2 = Node(name="expand_2", value_dict={"3": "c", "4": "d"})
        reduce_op = ReduceOp()
        reduced_node = reduce_op([expand_1, expand_2])
        self.assertEqual(len(reduced_node), 1)
        self.assertIn("1 3", reduced_node[0].value_dict)
        self.assertIn("2 4", reduced_node[0].value_dict)

    def test_reduce_op_one_empty_dict(self):
        expand_1 = Node(name="expand_1", value_dict={"1": "a", "2": "b"})
        expand_2 = Node(name="expand_2", value_dict={})
        reduce_op = ReduceOp()
        reduced_node = reduce_op([expand_1, expand_2])
        self.assertEqual(len(reduced_node), 1)
        self.assertEqual(reduced_node[0].value_dict, {})

    def test_reduce_op_both_empty_dicts(self):
        expand_1 = Node(name="expand_1", value_dict={})
        expand_2 = Node(name="expand_2", value_dict={})
        reduce_op = ReduceOp()
        reduced_node = reduce_op([expand_1, expand_2])
        self.assertEqual(len(reduced_node), 1)
        self.assertEqual(reduced_node[0].value_dict, {})


if __name__ == "__main__":
    unittest.main()
