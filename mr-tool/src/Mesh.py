import vedo


class Mesh:
    _vedo_mesh: vedo.Mesh

    _class: str
    _name: str

    def __init__(self, load_path: str):
        self._vedo_mesh = vedo.load(load_path)

        if self._vedo_mesh is None:
            print("Could not load " + load_path)
            exit(-1)

        path_tokens = load_path.split('/')
        self._class = path_tokens[len(path_tokens) - 2]
        self._name = path_tokens[-1]

    def subdivide(self, no_iterations: int):
        vedo_copy = self._vedo_mesh.copy()
        self._vedo_mesh = vedo_copy.subdivide(no_iterations)

    def decimate(self, no_fraction: float):
        vedo_copy = self._vedo_mesh.copy()
        self._vedo_mesh = vedo_copy.decimate(no_fraction)

    def get_class(self):
        return self._class

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

    def get_statistics(self):
        n = self._name
        c = self._class
        v = self.get_vertices()
        f = self.get_cells()
        t = self.get_no_triangles()
        q = self.get_no_quads()
        bb = self._vedo_mesh.box().bounds().tolist()

        return [n, c, v, f, t, q, bb]

    @property
    def vedo_mesh(self):
        return self._vedo_mesh

    @property
    def name(self):
        return self._name


# Just a wrapper class
class MeshStats:

    def __init__(self, n: str, c: str, v: int, f: int, t: int, q: int):
        self._name = n
        self._class = c
        self._no_vertices = v
        self._no_cells = f
        self._no_triangles = t
        self._no_quads = q

    @property
    def no_cells(self):
        return self._no_cells

    @property
    def no_vertices(self):
        return self._no_vertices

    @property
    def name(self):
        return self._name
