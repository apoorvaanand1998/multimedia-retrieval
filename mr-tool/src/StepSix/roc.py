import Mesh as M
import basic_metrics as B
import sklearn.metrics as SK
import presix as pre
import matplotlib.pyplot as plt

def roc(input_c_mesh, k, mthd):
    '''mthd = 'euc' or 'hnsw' '''
    res, scores = pre.df_to_meshes(pre.which_method(mthd, input_c_mesh), k)
    trues       = B.in_it(input_c_mesh, res)
    auroc       = SK.roc_auc_score(trues, scores)
    fpr, tpr, _ = SK.roc_curve(trues, scores)
    p           = SK.RocCurveDisplay(fpr=fpr, tpr=tpr, roc_auc=auroc)
    p.plot()
    plt.show()
    return auroc

def acc(input_c_mesh, k, mthd):
    pass

def sn_sp(inp: M.Mesh, res: list[M.Mesh]) -> tuple[float, float]:
    '''(Sensitivity, Specificity)'''
    tp, fp, tn, fn = B.get_basic_metrics(inp, res)

    return (tp / (tp + fn), tn / (fp + tn))

print(roc('Bed/D00121', 142, 'hnsw'))