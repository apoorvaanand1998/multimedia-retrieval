import csv
import numpy as np
import pathlib as p
import itertools
import ast


def get_vec(d: str, c_mesh: str, db: str) -> tuple[np.ndarray, np.ndarray]:
    """ c_mesh = 'Class/Mesh' e.g., 'Car/D00168'
    d is one of 'a3', 'd1', 'd2', 'd3', 'd4' """
    return row_to_hb(pick_row(d, c_mesh, db))


def pick_row(d: str, c_mesh: str, db: str) -> str:
    c, m = c_mesh.split('/')

    ## the paths here (ctrl + f 'path') might need to be changed for windows
    csv_path = '../../Output/ShapePropDesc/' + c + '.csv'  # path1
    nicks = ['RoundTable', 'Shelf', 'Ship', 'Sign', 'Skyscraper', 'Spoon', 'Starship', 'SubmachineGun', 'Sword', 'Tool',
             'Train', 'Tree', 'Truck']
    if c in nicks:
        csv_path = '../../Output/output_nick_untiltruck/Output' + c + '.csv'  # path2

    from_path = p.Path('../../' + db + '/' + c)  # path3
    names = [f.with_suffix('').name for f in from_path.iterdir()]
    n = len(names)
    i = names.index(m)
    ms = ['a3', 'd1', 'd2', 'd3', 'd4']
    calc_idx = i + ms.index(d) * n
    weird_mul = 2 if c in nicks else 1
    #
    # with open(csv_path, mode='r') as spd_file:
    #     spd_read = csv.reader(spd_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    #     r = next(itertools.islice(spd_read, calc_idx * weird_mul, None))
    #     return r

    with open(csv_path, mode='r') as spd_file:
        target_index = calc_idx * weird_mul
        try:
            # Attempt to retrieve the specified row
            spd_read = csv.reader(spd_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
            r = next(itertools.islice(spd_read, target_index, None))
            return r
        except StopIteration:
            print(f"Error: Reached end of file before reaching index {target_index}.")
            return None  # Or handle the case as needed, e.g., return an empty row or raise an exception


def row_to_hb(row: str) -> tuple[np.ndarray, np.ndarray]:
    if row is None:
        return None

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

# print(get_vec('d3', 'Bed/D00110'))
# print(get_vec('d3', 'Spoon/D00517'))