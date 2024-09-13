import vedo


##
# Wrapper class for the vedo mesh

class Mesh:
    _vedo_mesh: vedo.Mesh

    def __init__(self, vedo_mesh: vedo.Mesh):
        self._vedo_mesh = vedo_mesh

    def get_vertices(self):
        return self._vedo_mesh.dataset.GetNumberOfPoints()

    def get_cells(self):
        return self._vedo_mesh.dataset.GetNumberOfCells()

    def get_no_triangles(self):
        vertices = self._vedo_mesh.count_vertices()
        return vertices[vertices == 3].size

    def get_no_quads(self):
        vertices = self._vedo_mesh.count_vertices()
        return vertices[vertices == 4].size

