import sys

# These are used to "listen" to the executed code during the testing phase.
import io
old_stdout = sys.stdout
new_stdout = io.StringIO()

import ast
from copy import deepcopy
from itertools import product

from ast_util import prune

def ddminish(tree, nodes, test=None):
    """
    ddminish is a total search implementation of Andreas Zeller's delta debugging
    algorithm. Zeller's approach utilized a greedy binary-like search which is more
    efficient than the total search approach of this function.

    Parameters
    ----------
    tree : Python AST
        The AST that should be minimzed.
    nodes : [String]
        A list of strings representing pruneable nodes of the AST. These string
        can be acquired by using ast.dump(<your node>)
    test : currently UNUSED
    """
    max_pruned = 0
    min_config = None

    for configuration in [list(e) for e in product([0, 1], repeat=len(nodes))]:
        if (size := sum(configuration)) < max_pruned:
            continue

        nodes_to_prune = [nodes[i] for i, val in enumerate(configuration) if val]

        contender = deepcopy(tree)
        pruned_contender = prune(contender, nodes_to_prune)
        testable_contender = deepcopy(pruned_contender)
        # testable_contender.body.append(test)
        ast.fix_missing_locations(testable_contender)

        try:
            sys.stdout = new_stdout
            exec(compile(testable_contender, filename='<ast>', mode='exec'), {}, {})
            val = sys.stdout.getvalue()

            if "asdf" in val:
                min_config = deepcopy(pruned_contender)
                max_pruned = size
        
        except:
            pass
        
        finally:
            sys.stdout.seek(0)
            sys.stdout.truncate(0)
            sys.stdout = old_stdout
    
    return min_config

        
            