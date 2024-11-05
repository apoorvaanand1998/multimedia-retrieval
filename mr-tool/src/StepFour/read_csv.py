import csv
import numpy as np
import pathlib as p
import itertools
import ast

def get_vec(d: str, c_mesh: str) -> tuple[np.ndarray, np.ndarray]:
    """ c_mesh = 'Class/Mesh' e.g., 'Car/D00168'
    d is one of 'a3', 'd1', 'd2', 'd3', 'd4' """
    return row_to_hb(pick_row(d, c_mesh))

def pick_row(d: str, c_mesh: str) -> str:
    c, m = c_mesh.split('/')

    ## the paths here (ctrl + f 'path') might need to be changed for windows
    csv_path = '../../Output/ShapePropDesc2/' + c + '.csv' # path1
    from_path = p.Path('../../remeshed_normalized_filled_ShapeDB/' + c) # path3
    names     = [f.with_suffix('').name for f in from_path.iterdir()]
    n         = len(names)
    i         = names.index(m)
    ms        = ['a3', 'd1', 'd2', 'd3', 'd4']
    calc_idx  = i + ms.index(d) * n

    with open(csv_path, mode='r') as spd_file:
        spd_read = csv.reader(spd_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        r = next(itertools.islice(spd_read, calc_idx, None))
        return r

def row_to_hb(row: str) -> tuple[np.ndarray, np.ndarray]:
    h = row[1]
    h = h.replace("\n", "")
    h = h.replace(" ", "")
    h = h[7:]
    h = h.split("array(")
    h0 = h[0][:-2]
    h1 = h[1][:-2]
    h0 = np.array(ast.literal_eval(h0))
    h1 = np.array(ast.literal_eval(h1))
    return h0, h1

if __name__ == "__main__":
    print(get_vec('d4', 'Truck/D00241'))
    print(get_vec('d3', 'Spoon/D00517'))