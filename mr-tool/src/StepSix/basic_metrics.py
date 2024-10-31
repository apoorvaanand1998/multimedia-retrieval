import Mesh as M
import pathlib as P

ground_truth_path = P.Path('../../FINAL_remeshed_repaired_normalized_ShapeDB/')

def gt_meshes(p: P.Path) -> set[str]:
    return set([m.with_suffix('').name for m in p.iterdir()])

def get_basic_metrics(inp_mesh: M.Mesh, res_meshes: list[M.Mesh]) -> tuple[int, int, int, int]:
    ''' Returns tp, fp, tn, fn '''
    actual_meshes = gt_meshes(ground_truth_path + inp_mesh._class)

    tp = len(list(filter(lambda x : x in actual_meshes, res_meshes)))
    fp = len(list(filter(lambda x : x not in actual_meshes, res_meshes)))
    fn = len(list(filter(lambda x : x not in res_meshes, actual_meshes)))
    tn = 2483 - (tp + fp + fn) ## 2483 is the total number of meshes
    
    return tp, fp, tn, fn