from Mesh import Mesh, MeshStats
import numpy as np


def full_normalization(mesh: Mesh):
    translated_mesh = translate_to_origin(mesh)
    scaled_mesh = scale_to_unit_size(translated_mesh)
    aligned_mesh = align_principal_axes(scaled_mesh)
    flipped_mesh = flip_along_axes(aligned_mesh)

    return flipped_mesh

def translate_to_origin(mesh: Mesh) -> Mesh:
    processed_mesh: Mesh = mesh.__copy__()

    # From each vertex, substract the coordinates of the barycenter
    translated_points = []
    for point in processed_mesh.vedo_mesh.vertices:
        translated_points.append(point - processed_mesh.get_barycenter())
    processed_mesh.vedo_mesh.vertices = translated_points

    return processed_mesh


def scale_to_unit_size(mesh: Mesh) -> Mesh:
    processed_mesh: Mesh = mesh.__copy__()

    # Find largest AABB dimension
    sigma = max(mesh.get_bounding_box_dimensions())

    # Scale uniformly by dividing
    scaled_points = []
    for point in processed_mesh.vedo_mesh.vertices:
        scaled_points.append(point / sigma)
    processed_mesh.vedo_mesh.vertices = scaled_points

    return processed_mesh

def align_principal_axes(mesh: Mesh) -> Mesh:
    processed_mesh: Mesh = mesh.__copy__()

    cov = np.cov(mesh.vedo_mesh.vertices.T)  # 3x3 matrix
    eigenvalues, eigenvectors = np.linalg.eig(cov)

    # Sort by descending order
    sort_indices = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[sort_indices]
    eigenvectors = eigenvectors[:, sort_indices]

    # Build a rotation matrix from the top two eigenvectors
    # The first eigenvector aligns with the x-axis, and the second aligns with the y-axis.
    rotation_matrix = np.zeros((3, 3))
    rotation_matrix[:, 0] = eigenvectors[:, 0]  # First principal component -> x-axis
    rotation_matrix[:, 1] = eigenvectors[:, 1]  # Second principal component -> y-axis
    rotation_matrix[:, 2] = eigenvectors[:, 2]  # Third principal component -> z-axis

    # Rotate vertices
    processed_mesh.vedo_mesh.vertices = mesh.vedo_mesh.vertices @ rotation_matrix

    return processed_mesh

###
# Flipping along principal axes
# Must be done after PCA (align_principal_axes) normalization step
def flip_along_axes(mesh: Mesh) -> Mesh:
    processed_mesh: Mesh = mesh.__copy__()

    # Step 1: Compute the mean of each axis (the first moment)
    x_mean = np.mean(mesh.get_vertices()[:, 0])
    y_mean = np.mean(mesh.get_vertices()[:, 1])
    z_mean = np.mean(mesh.get_vertices()[:, 2])

    # Step 2: Initialize the flipped vertices as a copy of the original aligned vertices
    flipped_vertices = mesh.get_vertices().copy()

    # Step 3: Flip along the x-axis if needed
    if x_mean < 0:
        flipped_vertices[:, 0] *= -1
        # print("Flipped along the X-axis")

    # Step 4: Flip along the y-axis if needed
    if y_mean < 0:
        flipped_vertices[:, 1] *= -1
        # print("Flipped along the Y-axis")

    # Step 5: Flip along the z-axis if needed (optional, depends on your convention)
    if z_mean < 0:
        flipped_vertices[:, 2] *= -1
        # print("Flipped along the Z-axis")

    processed_mesh.vedo_mesh.vertices = flipped_vertices

    return processed_mesh


def main():
    mesh: Mesh = Mesh("../../remeshed_ShapeDB/AircraftBuoyant/m1337.obj")

main()