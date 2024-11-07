import Mesh as M
import basic_metrics as B
import sklearn.metrics as SK
import presix as pre
import matplotlib.pyplot as plt
import pathlib as P

def roc(input_c_mesh, k, mthd):
    '''mthd = 'euc' or 'hnsw'
       k = 142 (highest length of input class) '''
    res, scores = pre.df_to_meshes(pre.which_method(mthd, input_c_mesh), k)
    trues       = B.in_it(input_c_mesh, res)
    auroc       = SK.roc_auc_score(trues, scores)
    fpr, tpr, _ = SK.roc_curve(trues, scores)
    p           = SK.RocCurveDisplay(fpr=fpr, tpr=tpr, roc_auc=auroc)
    p.plot()
    plt.show()
    return auroc

def acc(input_c_mesh, mthd):
    '''k == length of input class'''
    c, _  = input_c_mesh.split('/')
    trues = sorted(list(B.gt_meshes(P.Path(str(B.ground_truth_path) + '/' + c))))
    r, _  = pre.df_to_meshes(pre.which_method(mthd, input_c_mesh), len(trues))
    r     = sorted(list(map(lambda x : x._name[:-4], r)))
    f     = lambda x : 1 if x in trues else 0
    r     = list(map(f, r))
    trues = [1] * len(trues)
    return SK.accuracy_score(trues, r)

def avg_p_score(input_c_mesh, mthd, k):
    res, scores = pre.df_to_meshes(pre.which_method(mthd, input_c_mesh), k)
    trues       = B.in_it(input_c_mesh, res)
    return SK.average_precision_score(trues, scores)

def bal_acc_score(input_c_mesh, mthd, k):
    '''avg of recall'''
    c, _  = input_c_mesh.split('/')
    trues = sorted(list(B.gt_meshes(P.Path(str(B.ground_truth_path) + '/' + c))))
    r, _  = pre.df_to_meshes(pre.which_method(mthd, input_c_mesh), k)
    r     = sorted(list(map(lambda x : x._name[:-4], r)))
    f     = lambda x : 1 if x in trues else 0
    r     = list(map(f, r))
    trues = [1] * len(trues)
    print(trues, r)
    return SK.balanced_accuracy_score(trues, r)

def sn_sp(inp: M.Mesh, res: list[M.Mesh]) -> tuple[float, float]:
    '''(Sensitivity, Specificity)'''
    tp, fp, tn, fn = B.get_basic_metrics(inp, res)

    return (tp / (tp + fn), tn / (fp + tn))

# print(roc('Bed/D00121', 142, 'hnsw'))
# print(avg_recall_score('Bed/D00121', 'euc', 27))
print(bal_acc_score('Bed/D00121', 'euc', 27))