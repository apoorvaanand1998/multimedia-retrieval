import logging

import vedo

def fill_holes(mesh: vedo.Mesh):
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
