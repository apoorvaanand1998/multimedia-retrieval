import os
import logging
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

def subdivide_meshes(source_dir, face_count_upper_bound=20000, target_vertices=5000, target_vertex_deviation=0.1):
    start_time = time.time()
    files = get_file_paths(source_dir)
    logging.info(f'Number of files: {len(files)}')

    broken_object_count = 0
    decimate_fail_count = 0
    total_point_count = 0
    for file in files:
        mesh = vd.load(file)
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
                logging.warning('Subdividing broke mesh')
                broken_object_count += 1
                is_broken_object = True
                break

        if is_broken_object:
            continue

        logging.info(f'Vertex count before 1st decimation routine: {mesh.dataset.GetNumberOfPoints()}')

        mesh.decimate(n=target_vertices)
        logging.info(f'Number of vertices after 1st decimation routine: {mesh.dataset.GetNumberOfPoints()}')
        current_fraction = target_vertices / mesh.dataset.GetNumberOfPoints()
        if current_fraction < 1:
            logging.info(f'Decimating by remaining fraction: {current_fraction}')
            mesh.decimate(fraction=current_fraction)
        elif current_fraction > 1.3:
            logging.warning('Too large overshot, skipping')
            decimate_fail_count += 1

        if 4900 < mesh.dataset.GetNumberOfPoints() < 5100:
            count = mesh.dataset.GetNumberOfPoints()
            logging.info(f'Successfully resampled to: {count}')
            total_point_count += count
        else:
            logging.warning(f'Failed at: {mesh.dataset.GetNumberOfPoints()}')
            decimate_fail_count += 1

        logging.info('')

    average_vertex_count = total_point_count / (len(files) - decimate_fail_count - broken_object_count)
    end_time = time.time()
    elapsed_time = end_time - start_time
    logging.info(f'Broken object count: {broken_object_count}')
    logging.info(f'Overshot decimate/subdivide count: {decimate_fail_count}')
    logging.info(f'Average vertex count: {average_vertex_count}')
    logging.info(f'Elapsed time: {elapsed_time}')

if __name__ == "__main__":
    source_directory = 'ShapeDB_sample'
    subdivide_meshes(source_directory)