import a_three as a3
import d_one as d1
import d_two as d2
import d_three as d3
import d_four as d4
import vedo
from matplotlib import pyplot as plt
import pathlib as p
import csv
import numpy as np

shape_db_path = '../../FINAL_remeshed_repaired_normalized_ShapeDB/'

def write_hists(cls: str, mthd: str, dst: str):
    """ Write histogram data from class cls,
        using mthd descriptor,
        into destination dst """

    from_path = p.Path(shape_db_path + cls)
    objs      = [x for x in from_path.iterdir()]
    strd_objs = sorted([str(o) for o in objs])
    loaded    = [vedo.load(o) for o in strd_objs]
    run_mthd  = lambda x : [x(l) for l in loaded]
    
    match mthd:
        case 'a3':
            res = run_mthd(a3.a3)
        case 'd1':
            res = run_mthd(d1.d1)
        case 'd2':
            res = run_mthd(d2.d2)
        case 'd3':
            res = run_mthd(d3.d3)
        case 'd4':
            res = run_mthd(d4.d4)
        case _:
            print('Use one of "a3", "d1" etc as arguments')
            res = []
    plt.title(mthd + ' for ' + cls)
    plt.savefig(dst+mthd+'_'+cls+'.png')
    plt.show()

    sob = [(mthd, s) for s in strd_objs]
    res = zip(sob, res)
    with open(dst+cls+'.csv', mode='a') as sd:
        sdw = csv.writer(sd, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        _   = [sdw.writerow(r) for r in res]

cs = p.Path(shape_db_path)
cs = sorted([c.name for c in cs.iterdir()])
np.set_printoptions(threshold=np.inf)
for c in cs:
    for m in ['a3', 'd1', 'd2', 'd3', 'd4']:
        write_hists(c, m, '../../Output/ShapePropDesc2/')