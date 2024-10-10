from resample_open3d import get_file_paths
import vedo as vd


def fill_holes_vedo(mesh):
    return mesh.fill_holes()


def export_mesh(mesh, file_path: str):
    mesh.write(file_path)


if __name__ == "__main__":
    source_directory = "remeshed_ShapeDB"
    destination_directory = "remeshed_normailzed_filled_ShapeDB"
    files, destination_files = get_file_paths(source_directory, destination_directory)

    filled_shape_count = 0
    for file_index, file in enumerate(files[:100]):
        current_mesh = vd.load(file)
        fixed_mesh = fill_holes_vedo(current_mesh)

        if current_mesh.dataset.GetNumberOfCells() < fixed_mesh.dataset.GetNumberOfCells():
            filled_shape_count += 1

        export_mesh(fixed_mesh, destination_files[file_index])
    print(filled_shape_count)

