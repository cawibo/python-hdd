from ast_util import tag_nodes
from dd import ddminish

def hdd(tree, test=None):
    """
    HDD, or Hierarchical Delta Debugging, is an extension of Andreas Zeller's
    Delta Debugging algorithm. Instead of treating the whole input as consisting
    of equally valuable atomic parts, HDD retains information about the structure.
    This allows for a more structured strategy for pruning ( for the case )
    unnecessary elements.

    Formal definition of HDD can be found at https://people.inf.ethz.ch/suz/publications/icse06-hdd.pdf

    Parameters
    ----------
    tree : Python AST
        The AST that should be minimzed.
    test : currently UNUSED
    """
    level = 0
    nodes = tag_nodes(tree, level)
    
    while nodes:
        min_config = ddminish(tree, nodes, test)
        if min_config is not None:
            tree = min_config
        
        level += 1
        nodes = tag_nodes(tree, level)

    return tree