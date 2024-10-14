import open3d as o3d
import numpy as np
from resample_open3d import get_file_paths


def calculate_volume(vertices: np.ndarray, triangles: np.ndarray):
    total_volume = 0
    origin = np.array([0.0, 0.0, 0.0])

    for tri in triangles:
        x1 = vertices[tri[0]]
        x2 = vertices[tri[1]]
        x3 = vertices[tri[2]]

        v1 = x1 - origin
        v2 = x2 - origin
        v3 = x3 - origin

        cross_product = np.cross(v1, v2)
        volume_tetrahedron = np.dot(cross_product, v3)

        total_volume += volume_tetrahedron

    return abs(total_volume) / 6


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


def get_global_descriptors(mesh: o3d.geometry.TriangleMesh) -> dict[str, float]:
    shape_volume = calculate_volume(np.asarray(mesh.vertices), np.asarray(mesh.triangles))
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

    # EXAMPLE USAGE
    o3d_sphere = o3d.geometry.TriangleMesh.create_sphere()
    global_descriptor_sphere = get_global_descriptors(o3d_sphere)

    o3d_box = o3d.geometry.TriangleMesh.create_box(width=2)
    global_descriptor_box = get_global_descriptors(o3d_box)

