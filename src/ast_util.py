import ast

class Prune(ast.NodeTransformer):
    """
    A simple implementation of a pruner that traverses
    the given tree and prunes any nodes that are also
    found in self.nodes.

    Parameters
    ----------
    nodes : [String]
        A list of strings representing pruneable nodes of the AST. These string
        can be acquired by using ast.dump(<your node>)
    """

    def __init__(self, nodes):
        self.nodes = nodes

    def visit(self, node):
        res = None

        # the default root of Python code is Module,
        # it should never be pruned.
        if isinstance(node, ast.Module):
            res = node

        # prune if node is one of the prune-assigned nodes
        if ast.dump(node) not in self.nodes:
            res = node

        self.generic_visit(node)
        return res

def prune(tree, nodes):
    """
    Prunes :nodes: from :tree:.

    Parameters
    ----------
    tree : Python AST
        The AST that should be pruned.
    nodes : [AST]
        A list of AST-nodes that should be pruned (if found) in :tree:
    """
    nodes = [ast.dump(node) for node in nodes]

    pruned_tree = Prune(nodes).visit(tree)

    # pruning will alter the AST location info
    ast.fix_missing_locations(pruned_tree)

    return pruned_tree

def tag_nodes(tree, target_level=0):
    """
    Returns a list with all AST elements found at the :target_level:.

    Parameters
    ----------
    tree : Python AST
        The AST to traverse.
    target_level : Integer
        The level at which to locate nodes. Default is 0.
    """
    nodes = []

    def inner_tag_nodes(node, current_level):
        for child in ast.iter_child_nodes(node):
            if target_level == current_level:
                nodes.append(child)
                continue

            inner_tag_nodes(child, current_level + 1)
        
    inner_tag_nodes(tree, 0)

    return nodes