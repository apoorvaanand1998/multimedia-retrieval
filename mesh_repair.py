from resample_open3d import get_file_paths
import vedo as vd
import open3d as o3d
import numpy as np


def export_mesh(mesh, file_path: str):
    mesh.write(file_path)

def fix(mesh: o3d.geometry.TriangleMesh) -> o3d.geometry.TriangleMesh:
    if mesh.get_non_manifold_edges():
        print("found non-manifold edges: ", mesh.get_non_manifold_edges())
        mesh.remove_non_manifold_edges()
    if mesh.is_self_intersecting():
        print("i cry everytime")



if __name__ == "__main__":
    source_directory = "remeshed_ShapeDB"
    destination_directory = "remeshed_normailzed_filled_ShapeDB"
    files, destination_files = get_file_paths(source_directory, destination_directory)

    filled_shape_count = 0
    for file_index, file in enumerate(files[:50]):
        current_mesh = o3d.io.read_triangle_mesh(file)
        fixed_mesh = fix(current_mesh)
        #check_watertightness(fixed_mesh)
        #if current_mesh.dataset.GetNumberOfCells() < fixed_mesh.dataset.GetNumberOfCells():
          #  filled_shape_count += 1

        #export_mesh(fixed_mesh, destination_files[file_index])
    #print(filled_shape_count)

