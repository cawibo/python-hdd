import unittest
import ast, inspect
from copy import deepcopy

from ..ast_util import *

hello_world_source = """
print("hello world")
"""
arithmetic_source = """
a = 10
b = 20
c = a + b
print(c)
"""
arithmetic_source_no_print = """
a = 10
b = 20
c = a + b
"""
print_call_node = ast.Expr(
            value=ast.Call(
                func=ast.Name(id='print', ctx=ast.Load()),
                args=[ast.Name(id='c', ctx=ast.Load())],
                keywords=[]
            ))

class TestPruning(unittest.TestCase):
    def test_empty_nodes_in_prune_should_not_alter_ast(self):
        arithmetic_ast = ast.parse(arithmetic_source)

        actual = prune(deepcopy(arithmetic_ast), [])

        self.assertEqual(ast.dump(actual), ast.dump(arithmetic_ast))

    def test_irrelevant_nodes_in_prune_should_not_alter_ast(self):
        arithmetic_ast = ast.parse(arithmetic_source)
        nodes = [ast.Call(), ast.Pass(), ast.Div()]

        actual = prune(deepcopy(arithmetic_ast), nodes)

        self.assertEqual(ast.dump(actual), ast.dump(arithmetic_ast))

    def test_matching_nodes_in_prune_should_alter_ast(self):
        arithmetic_ast = ast.parse(arithmetic_source)
        nodes = [deepcopy(print_call_node)]

        actual = prune(deepcopy(arithmetic_ast), nodes)

        self.assertNotEqual(ast.dump(actual), ast.dump(arithmetic_ast))
        
    def test_only_matching_nodes_should_be_pruned(self):
        arithmetic_ast = ast.parse(arithmetic_source)
        nodes = [deepcopy(print_call_node)]

        actual = prune(deepcopy(arithmetic_ast), nodes)

        expected = ast.parse(arithmetic_source_no_print)
        self.assertEqual(ast.dump(actual), ast.dump(expected))

class TestTagging(unittest.TestCase):
    def test_root_level_empty_source(self):
        test_ast = ast.parse("")

        actual = tag_nodes(test_ast)

        self.assertEqual(len(actual), 0)
        
    def test_level_should_default_to_0(self):
        test_ast = ast.parse(arithmetic_source)

        expected = tag_nodes(test_ast, 0)
        actual = tag_nodes(test_ast)

        self.assertEqual(actual, expected)

    def test_non_root(self):
        test_ast = ast.parse(arithmetic_source_no_print)

        actual = tag_nodes(test_ast, 1)

        self.assertTrue(
            isinstance(actual[1], ast.Constant) and
            isinstance(actual[2], ast.Name) and
            isinstance(actual[3], ast.Constant) and
            isinstance(actual[4], ast.Name) and
            isinstance(actual[0], ast.Name) and
            isinstance(actual[5], ast.BinOp)
        )

if __name__ == '__main__':
    unittest.main()