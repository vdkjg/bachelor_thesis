import os
import time

import clingo
from minimal_unsatisfiable_core import Util, MUC

from clingraph.orm import Factbase
from clingraph.graphviz import compute_graphs, render


def muc_sudoku():
    assumption_list = [
        # adding assumptions
        # CORRECT ASSUMPTIONS
        # TODO : is the (_, True) necessary?
        (clingo.Function("guess", [clingo.Number(4), clingo.Number(9), clingo.Number(3)]), True),
        (clingo.Function("guess", [clingo.Number(7), clingo.Number(1), clingo.Number(9)]), True),
        (clingo.Function("guess", [clingo.Number(2), clingo.Number(2), clingo.Number(7)]), True),
        (clingo.Function("guess", [clingo.Number(5), clingo.Number(7), clingo.Number(7)]), True),
        (clingo.Function("guess", [clingo.Number(3), clingo.Number(9), clingo.Number(7)]), True),
        (clingo.Function("guess", [clingo.Number(8), clingo.Number(2), clingo.Number(8)]), True),
        (clingo.Function("guess", [clingo.Number(1), clingo.Number(6), clingo.Number(8)]), True),
        (clingo.Function("guess", [clingo.Number(6), clingo.Number(7), clingo.Number(8)]), True),
        (clingo.Function("guess", [clingo.Number(2), clingo.Number(9), clingo.Number(8)]), True),
        # CONFLICTING ASSUMPTIONS
        # double value for cell
        # (clingo.Function("guess", [clingo.Number(4), clingo.Number(9), clingo.Number(5)]), True),
        # value at the wrong position in cage (double 7 in cage(1,1))
        # (clingo.Function("guess", [clingo.Number(2), clingo.Number(3), clingo.Number(7)]), True),
    ]

    program = "res/sudoku_only_rules.lp"
    instance = "res/instances/sudoku_instance_1.lp"
    visualization = "res/visualization/visualize_sudoku.lp"

    print("T0 : SOLVING START")
    # TODO : cannot use the solve handle outside the function. Is this bc of async/parallel programming?
    (satisfiable, model_string, core) = Util.solve(
        program=program,
        instance=instance,
        assumption_list=assumption_list
    )

    print("result : ", ["UNSAT", "SAT"][satisfiable])
    print("model : ", model_string)
    print("core : ", core)

    if satisfiable:
        Util.render_sudoku(model_string, visualization_file=visualization)

    print("T0 : SOLVING END")
    print("T1 : FINDING MUC START")

    unsatisfiable, muc = MUC.muc_iterative_deletion(
        program=program,
        instance=instance,
        assumption_list=assumption_list
    )

    if not unsatisfiable:
        print("MUC : Problem wasn't unsatisfiable to begin with, there is no minimal unsatisfiable core")
    else:
        print(f"MUC : {muc}")

    print("T1 : FINDING MUC END")

    # TODO : what do the ints in the uc mean ???


if __name__ == '__main__':
    # example_clingraph()
    muc_sudoku()

