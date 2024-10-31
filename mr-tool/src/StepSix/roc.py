import Mesh as M
import basic_metrics as B
from typing import Callable

def roc(f: Callable[[M.Mesh, int], list[M.Mesh]], 
        inp: M.Mesh, start: int, stop: int, step: int) -> int:
    # ''' Returns AUROC '''
    # sn_sps = []
    # for i in range(start, stop, step):
    #     curr   = sn_sp(inp, f(inp, i))
    #     sn_sps.append(curr)
    # sn_sps = sorted(sn_sps, lambda x : x[0])

def sn_sp(inp: M.Mesh, res: list[M.Mesh]) -> tuple[float, float]:
    '''(Sensitivity, Specificity)'''
    tp, fp, tn, fn = B.get_basic_metrics(inp, res)

    return (tp / (tp + fn), tn / (fp + tn))