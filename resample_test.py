import os
import logging
from pdb import post_mortem

import vedo as vd
import time

logging.basicConfig(filename='subdivide_meshes.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def get_file_paths(source_dir):
    files = []

    for subdir in os.listdir(source_dir):
        subdir_path = os.path.join(source_dir, subdir)
        if os.path.isdir(subdir_path):
            for file in os.listdir(os.path.join(source_dir, subdir)):
                files.append(os.path.join(source_dir, subdir, file))

    return files


def resample_mashes(source_dir, face_count_upper_bound=30000, target_vertices=5000, target_vertex_deviation=500, fraction_step=0.1):
    start_time = time.time()
    files = get_file_paths(source_dir)
    logging.info(f'Number of files: {len(files)} || Target faces: {face_count_upper_bound} || Target vertices: {target_vertices}')


    broken_object_count = 0
    decimate_fail_count = 0
    total_point_count = 0
    for file in files:
        mesh = vd.load(file)
        logging.info('')
        logging.info(f'Loaded: {file}')

        current_face_count = mesh.dataset.GetNumberOfCells()
        current_iteration = 0
        is_broken_object = False
        while current_face_count < face_count_upper_bound:
            current_iteration += 1
            logging.info(f'Subdividing: {mesh.dataset.GetNumberOfCells()} faces')
            mesh.subdivide(n=1)
            current_face_count = mesh.dataset.GetNumberOfCells()

            if current_face_count == 0:
                logging.critical('Subdividing broke mesh')
                broken_object_count += 1
                is_broken_object = True
                break

        if is_broken_object:
            continue

        current_vertex_count = mesh.dataset.GetNumberOfPoints()
        logging.info(f'Vertex count before decimation routine: {current_vertex_count}')

        current_iteration = 0
        decimation_fraction = 1 - fraction_step
        logging.info(f'Decimating...')
        while current_vertex_count > target_vertices + target_vertex_deviation:
            current_iteration += 1

            if current_iteration > 50:
                logging.warning('Decimation routine failed')
                break

            mesh.decimate(fraction=decimation_fraction)
            current_vertex_count = mesh.dataset.GetNumberOfPoints()

        if target_vertices - target_vertex_deviation < current_vertex_count < target_vertices + target_vertex_deviation:
            count = mesh.dataset.GetNumberOfPoints()
            logging.info(f'Successfully resampled to: {count}')
            logging.info(f'Decimation iterations: {current_iteration}')
            total_point_count += count
            #### SAVE HERE
        else:
            logging.warning(f'Failed at: {mesh.dataset.GetNumberOfPoints()}')
            decimate_fail_count += 1


    average_vertex_count = total_point_count / (len(files) - decimate_fail_count - broken_object_count)
    end_time = time.time()
    elapsed_time = end_time - start_time
    logging.info(f'Broken object count: {broken_object_count}')
    logging.info(f'Overshot decimate count: {decimate_fail_count}')
    logging.info(f'Average vertex count: {average_vertex_count}')
    logging.info(f'Elapsed time: {elapsed_time}')

if __name__ == "__main__":
    source_directory = 'ShapeDB_sample'
    resample_mashes(source_directory)