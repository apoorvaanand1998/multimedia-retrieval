import os
import logging
import time
import open3d as o3d
import numpy as np
import vedo

from Mesh import Mesh
from global_descriptors import fromVedoToOpen3DMesh

logging.basicConfig(filename='remesh.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def get_file_paths(source_dir, dest_dir) -> tuple[list[str], list[str]]:
    source_file_paths = []
    destination_file_paths = []

    for subdir in os.listdir(source_dir):
        subdir_path = os.path.join(source_dir, subdir)
        if os.path.isdir(subdir_path):
            dest_subdir_path = os.path.join(dest_dir, subdir)

            if not os.path.exists(dest_subdir_path):
                os.makedirs(dest_subdir_path)

            for file in os.listdir(os.path.join(source_dir, subdir)):
                source_file_paths.append(os.path.join(source_dir, subdir, file))
                destination_file_paths.append(os.path.join(dest_subdir_path, file))

    return source_file_paths, destination_file_paths


def create_directory(dest_dir, subdir):
    dest_subdir_path = os.path.join(dest_dir, subdir)
    if not os.path.exists(dest_subdir_path):
        os.makedirs(dest_subdir_path)

    return dest_subdir_path


def resample_mashes(source_dir, dest_dir, face_count_upper_bound=30000, target_vertices=5000,
                    target_vertex_deviation=500, fraction_step=0.1):
    start_time = time.time()
    files, dest_files = get_file_paths(source_dir, dest_dir)

    logging.info(
        f'Number of files: {len(files)} || Target faces: {face_count_upper_bound} || Target vertices: {target_vertices}')

    broken_object_count = 0
    decimate_fail_count = 0
    total_point_count = 0
    for file in files:
        o3d_mesh = o3d.io.read_triangle_mesh(file)
        logging.info('')
        logging.info(f'Loaded: {file}')

        current_face_count = len(np.asarray(o3d_mesh.triangles))
        current_iteration = 0
        is_broken_object = False
        new_object = o3d_mesh
        while current_face_count < face_count_upper_bound:
            current_iteration += 1
            logging.info(f'Subdividing: {current_face_count} faces')

            new_object = new_object.subdivide_midpoint(1)
            current_face_count = len(np.asarray(new_object.triangles))

            if current_face_count == 0:
                logging.critical('Subdividing broke mesh')
                broken_object_count += 1
                is_broken_object = True
                break

        if is_broken_object:
            continue

        current_vertex_count = len(np.asarray(new_object.vertices))
        logging.info(f'Vertex count before decimation routine: {current_vertex_count}')

        logging.info(f'Decimating...')

        fraction_target_vertices = target_vertices / current_vertex_count
        target_faces = int(current_face_count * fraction_target_vertices)

        decimated_object = new_object.simplify_quadric_decimation(target_faces)
        current_vertex_count = len(np.asarray(decimated_object.vertices))

        if target_vertices - target_vertex_deviation < current_vertex_count < target_vertices + target_vertex_deviation:
            logging.info(f'Successfully resampled to: {current_vertex_count} vertices')
            total_point_count += current_vertex_count
            o3d.io.write_triangle_mesh(dest_files[files.index(file)], decimated_object)
        else:
            logging.warning(f'Failed decimating at: {current_vertex_count} vertices')
            decimate_fail_count += 1
            o3d.io.write_triangle_mesh(dest_files[files.index(file)], decimated_object)

    average_vertex_count = total_point_count / (len(files) - decimate_fail_count - broken_object_count)
    end_time = time.time()
    elapsed_time = end_time - start_time
    logging.info('')
    logging.info(f'Broken object count: {broken_object_count}')
    logging.info(f'Overshot decimate count: {decimate_fail_count}')
    logging.info(f'Average vertex (successfully decimated) count: {average_vertex_count}')
    logging.info(f'Elapsed time: {elapsed_time}')


def fromOpen3DToVedoMesh(o3d_mesh: o3d.geometry.TriangleMesh) -> vedo.Mesh:
    # Extract vertices and faces from the Open3D mesh
    vertices = np.asarray(o3d_mesh.vertices)  # Convert to numpy array
    faces = np.asarray(o3d_mesh.triangles)  # Convert to numpy array

    # Create a Vedo Mesh from vertices and faces
    vedo_mesh = vedo.Mesh([vertices, faces])

    return vedo_mesh


########
# USED BY MAIN APP
#######
def resample_mesh(mesh: Mesh, face_count_upper_bound=30000, target_vertices=5000, target_vertex_deviation=500) -> Mesh:
    o3d_mesh = fromVedoToOpen3DMesh(mesh.vedo_mesh)
    current_face_count = len(np.asarray(o3d_mesh.triangles))
    current_iteration = 0
    is_broken_object = False
    new_object = o3d_mesh
    while current_face_count < face_count_upper_bound:
        current_iteration += 1
        logging.info(f'Subdividing: {current_face_count} faces')

        new_object = new_object.subdivide_midpoint(1)
        current_face_count = len(np.asarray(new_object.triangles))

        if current_face_count == 0:
            logging.critical('Subdividing broke mesh')
            is_broken_object = True
            break

    current_vertex_count = len(np.asarray(new_object.vertices))
    logging.info(f'Vertex count before decimation routine: {current_vertex_count}')

    logging.info(f'Decimating...')

    fraction_target_vertices = target_vertices / current_vertex_count
    target_faces = int(current_face_count * fraction_target_vertices)

    decimated_object = new_object.simplify_quadric_decimation(target_faces)
    current_vertex_count = len(np.asarray(decimated_object.vertices))

    if is_broken_object:
        return None

    resampled_mesh = mesh.__copy__()
    vedo_mesh = fromOpen3DToVedoMesh(new_object)
    resampled_mesh._vedo_mesh = vedo_mesh
    return resampled_mesh


if __name__ == "__main__":
    source_directory = 'ShapeDB_sample'
    destination_directory = 'remeshed_ShapeDB'
    resample_mashes(source_directory, destination_directory)
