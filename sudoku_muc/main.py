import clingo
import time
from minimal_unsatisfiable_core import Util, Container


def muc_sudoku():

    example_directory = "res/examples/sudoku/sudoku_multi_combined"
    visualization = "res/visualization/visualize_sudoku_core.lp"
    render_sudoku = True

    container_1 = Container(
        example_directory=example_directory
    )

    print([container_1])
    print(container_1)

    satisfiable, model, core = container_1.solve()
    print("result : ", ["UNSAT", "SAT"][satisfiable])
    print("model : ", model)
    print("core : ", core)

    if render_sudoku:
        if satisfiable:
            Util.render_sudoku(model, visualization)
        else:
            Util.render_sudoku_with_core(container_1, core, visualization, name_format="1")

    print("FIND MUC ON CORE : ASSUMPTION MARKING")
    muc_found, muc = container_1.get_muc_on_core_assumption_marking()

    if render_sudoku and not satisfiable:
        Util.render_sudoku_with_core(container_1, muc, visualization, name_format="2")

    return

    if not muc_found:
        print("MUC : Problem wasn't unsatisfiable to begin with, there is no minimal unsatisfiable core")
    else:
        print(f"MUC : {muc}")

    time_bf_start = time.time()
    ucs = container_1.get_uc_all_brute_force()
    time_bf_end = time.time()

    time_bf_muc_start = time.time()
    mucs = container_1.get_all_minimal_ucs_brute_force()
    time_bf_muc_end = time.time()

    print("time BF All:", time_bf_end - time_bf_start, "s")
    print("time BF Minimal:", time_bf_muc_end - time_bf_muc_start, "s")

    return

    print("FIND UC ON ASSUMPTION SET : ITERATIVE DELETION")

    uc = container_1.get_uc_iterative_deletion()
    if uc:
        print("UC: ", [str(a) for a in uc])
    else:
        print("No UC was found")

    mucs = container_1.get_muc_all_iterative_deletion()
    if mucs:
        print("MUCs: \n", "\n".join(["\t+ " + " ".join([str(a) for a in core]) for core in mucs]))
    else:
        print("No MUCs were found")

    print("FIND ALL UCS : BRUTE FORCE APPROACH")

    ucs = container_1.get_uc_all_brute_force()
    print("Cores Found (Cores/|Assumption-Powerset|):", len(ucs), "/", 2**len(container_1.assumptions))
    minimum_ucs = container_1.get_minimum_ucs_brute_force()
    print("Minimum UCs Found: ", minimum_ucs)


if __name__ == '__main__':
    # example_clingraph()
    muc_sudoku()
    # clingraph_factbase_computation()

