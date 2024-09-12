from pathlib import PurePath
from vedo import load, Mesh, show
import numpy as np

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
    return b.bounds() ## ((min x, max x), (min y, max y), (min z), (max z))

print(bounding_box("../ShapeDatabase_INFOMR/Bed/D00031.obj", True))