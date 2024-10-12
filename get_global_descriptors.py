import open3d as o3d
import numpy as np
from resample_open3d import get_file_paths



def calculate_compactness(surface_area: float, shape_volume: float) -> float:
    return surface_area ** 3 / shape_volume ** 2


def calculate_diameter(hull_vertices: np.ndarray) -> float:
    max_distance = 0
    for i in range(len(hull_vertices)):
        for j in range(i + 1, len(hull_vertices)):
            distance = np.linalg.norm(hull_vertices[i] - hull_vertices[j])
            if distance > max_distance:
                max_distance = distance
    return max_distance


def get_global_descriptors(mesh: o3d.geometry.TriangleMesh) -> dict:
    shape_volume = mesh.get_volume()
    surface_area = mesh.get_surface_area()
    convex_hull = mesh.compute_convex_hull()[0]
    hull_volume = convex_hull.get_volume()
    oriented_bounding_box = mesh.get_oriented_bounding_box()
    obb_volume = oriented_bounding_box.volume()
    hull_vertices = np.asarray(convex_hull.vertices)
    covar_matrix = np.cov(np.transpose(np.asarray(mesh.vertices)))
    eigenvalues, _ = np.linalg.eig(covar_matrix)

    descriptors = {
        'surface_area': surface_area,
        'compactness': calculate_compactness(surface_area, shape_volume),
        'rectangularity': shape_volume / obb_volume,
        'diameter': calculate_diameter(hull_vertices),
        'convexity': shape_volume / hull_volume,
        'eccentricity': max(eigenvalues) / min(eigenvalues)
    }

    return descriptors

if __name__ == "__main__":
    source_directory = "remeshed_ShapeDB"
    destination_directory = "ShapeDB_sample_global_descriptors"
    o3d_sphere = o3d.geometry.TriangleMesh.create_sphere()

    global_descriptors = get_global_descriptors(o3d_sphere)
    print(global_descriptors)
    o3d_box = o3d.geometry.TriangleMesh.create_box(width=2)
    global_descriptors = get_global_descriptors(o3d_box)
    print(global_descriptors)
