import open3d as o3d
import vedo as vd
import numpy as np
from resample_open3d import get_file_paths
import trimesh as tm
import time

def get_global_descriptors(mesh: o3d.geometry.TriangleMesh, descriptor: str) -> float | None:
    convex_hull = mesh.compute_convex_hull()[0]
    if descriptor == 'surface_area':
        return mesh.get_surface_area()
    elif descriptor == 'compactness':
        calculate_compactness(mesh)
    elif descriptor == 'rectangularity':
        return
        #shape_volume = mesh.get_volume()
        #bounding_box = mesh.get_axis_aligned_bounding_box() # need oriented bounding box
        #return bounding_box.volume()
    elif descriptor == 'diameter':
        convex_hull = mesh.compute_convex_hull()[0]
        hull_vertices = np.asarray(convex_hull.vertices)
        max_distance = 0
        for i in range(len(hull_vertices)):
            for j in range(i + 1, len(hull_vertices)):
                distance = np.linalg.norm(hull_vertices[i] - hull_vertices[j])
                if distance > max_distance:
                    max_distance = distance
        return max_distance

def calculate_compactness(mesh: o3d.geometry.TriangleMesh) -> float:
    triangles = np.asarray(mesh.triangles)
    print(triangles)

if __name__ == "__main__":
    source_directory = "remeshed_ShapeDB"
    destination_directory = "ShapeDB_sample_global_descriptors"
    files, destination_files = get_file_paths(source_directory, destination_directory)
    for file in files[:1]:
        print(f"Processing: {file}")
        o3d_mesh = o3d.io.read_triangle_mesh(file)
        #surface_area = get_global_descriptors(o3d_mesh, 'surface_area')
        #compactness = get_global_descriptors(o3d_mesh, 'compactness')
        #rectangularity = get_global_descriptors(o3d_mesh, 'rectangularity')
        diameter = get_global_descriptors(o3d_mesh, 'diameter')
        #print(f"Surface Area: {surface_area}")
        #print(f"Compactness: {compactness}")
        p#rint(f"Rectangularity: {rectangularity}")
        print(f"Diameter: {diameter}")