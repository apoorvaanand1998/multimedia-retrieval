from pathlib import PurePath, Path
from vedo import load, Mesh, show
import numpy as np
import csv
from typing import TypeVar

def output_csv(shape_path: str, csv_path: str, ez_mode: bool=True) -> int:
    objs = concat(list_objs(shape_path, ez_mode))

    with open(csv_path, mode='w') as stat_file:
        stat_writer = csv.writer(stat_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for obj in objs:
            n  = str(obj)
            c  = shape_class(n)
            v  = n_o_vertices(n)
            f  = n_o_faces(n)
            tq = n_o_triangles_quads(n)
            bb = bounding_box(n).tolist()

            stat_writer.writerow([n, c, v, f, tq, bb])
    
    return len(objs)

def list_objs(shape_path: str, ez_mode: bool=True) -> list[list[Path]]:
    p    = Path(shape_path)
    dirs = [d for d in p.iterdir() if d.is_dir()]
    objg = [d.iterdir() for d in dirs]
    objs = [list(g) for g in objg]

    if ez_mode: 
        objs = [o[0:3] for o in objs]

    return objs

def shape_class(file_path: str) -> str:
    return PurePath(file_path).parent.name

def n_o_vertices(file_path: str) -> int:
    mesh = load(file_path)
    return mesh.dataset.GetNumberOfPoints()

def n_o_faces(file_path: str) -> int:
    mesh = load(file_path)
    return mesh.dataset.GetNumberOfCells()

def n_o_triangles_quads(file_path: str) -> tuple[int, int]:
    mesh = load(file_path)
    varr = mesh.count_vertices()
    return (varr[varr == 3].size, varr[varr == 4].size) 
    ## weird sytax for filtering numpy arrays

def bounding_box(file_path: str, show_box: bool=False) -> np.ndarray:
    mesh = load(file_path)
    b    = mesh.box()
    if show_box: 
        show(mesh, b)
        print(b)
    return b.bounds() ## [min x, max x, min y, max y, min z, max z]

T = TypeVar('T')
def concat(xss: list[list[T]]) -> list[T]: 
    ## aka flatten
    return [x for xs in xss for x in xs]

print(output_csv("../ShapeDatabase_INFOMR", "../Output/stats.csv"))