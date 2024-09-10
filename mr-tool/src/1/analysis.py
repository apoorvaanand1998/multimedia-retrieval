from pathlib import PurePath
from vedo import load, show

def shape_class(file_path: str, ez: bool=True) -> str:
    return PurePath(file_path).parent.name

def n_o_vertices(file_path: str) -> int:
    mesh = load(file_path)
    return mesh.dataset.GetNumberOfPoints()

def n_o_faces(file_path: str) -> int:
    mesh = load(file_path)
    return mesh.dataset.GetNumberOfCells()

print(n_o_faces("../ShapeDatabase_INFOMR/Bed/D00031.obj"))