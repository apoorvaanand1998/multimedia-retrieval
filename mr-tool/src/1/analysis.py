from pathlib import PurePath
from vedo import load, Mesh

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

print(n_o_triangles_quads("../ShapeDatabase_INFOMR/Bed/D00031.obj"))