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

def in_it(c_mesh, res: list[M.Mesh]):
    c, _ = c_mesh.split('/')
    actuals = gt_meshes(P.Path(str(ground_truth_path) + '/' + c))
    res     = list(map(lambda x : x._name, res))
    f       = lambda x : 1 if x in map(lambda x : x + '.obj', actuals) else 0
    return list(map(f, res))

#print(in_it('Bed/D00121', [M.Mesh('../../FINAL_remeshed_repaired_normalized_ShapeDB/Bed/D00121.obj')]))