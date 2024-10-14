from resample_open3d import get_file_paths
import vedo as vd
import logging

logging.basicConfig(filename='repair_files.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def fix(mesh):
    if mesh.is_closed():
        logging.info("Mesh is watertight")
        return mesh, False
    else:
        no_cells = mesh.dataset.GetNumberOfCells()
        logging.info(f"Mesh is not watertight current number of cells: {no_cells} ")

        mesh_copy = mesh.clone()
        mesh_copy.fill_holes(size=0.1)

        no_cells_after = mesh_copy.dataset.GetNumberOfCells()
        logging.info(f"Mesh is now watertight new number of cells: {no_cells_after}")

        return mesh_copy, True


def export_mesh(mesh, file_path: str):
    mesh.write(file_path)


if __name__ == "__main__":
    source_directory = "remeshed_ShapeDB"
    destination_directory = "remeshed_normailzed_filled_ShapeDB"

    files, destination_files = get_file_paths(source_directory, destination_directory)

    filled_shape_count = 0
    for file_index, file in enumerate(files[:50]):
        current_mesh = vd.load(file)
        logging.info(f'Loaded: {file}')
        fixed_mesh, is_filled = fix(current_mesh)

        if is_filled:
            filled_shape_count += 1

        logging.info(f"Exporting mesh to {destination_files[file_index]}")
        export_mesh(fixed_mesh, destination_files[file_index])
