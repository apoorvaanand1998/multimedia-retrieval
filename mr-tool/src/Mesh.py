import math

import numpy as np
import vedo


class Mesh:
    _path: str
    _vedo_mesh: vedo.Mesh

    _class: str
    _name: str

    def __init__(self, load_path: str):
        self._path = load_path

        self._vedo_mesh = vedo.load(load_path)

        if self._vedo_mesh is None:
            print("Could not load " + load_path)
            raise(Exception("Could not load " + load_path))

        path_tokens = load_path.split('/')
        self._class = path_tokens[len(path_tokens) - 2]
        self._name = path_tokens[-1]

    def __copy__(self):
        return Mesh(self._path)

    def get_value_of_largest_bbox_dimension(self):
        dim = self.get_bounding_box_dimensions()
        for d in dim:
            if math.isnan(d):
                print('x')
                a = self._vedo_mesh.bounds()
                box = self._vedo_mesh.box()
                aabb_bounds = self._vedo_mesh.box().box().bounds()
                aabb_dimensions = [
                    aabb_bounds[1] - aabb_bounds[0],
                    aabb_bounds[3] - aabb_bounds[2],
                    aabb_bounds[5] - aabb_bounds[4]
                ]

        return np.array(self.get_bounding_box_dimensions()).max()

    def translate_to_world_origin(self):
        # From each vertex, substract the coordinates of the barycenter
        translated_points = []
        for point in self._vedo_mesh.vertices:
            translated_points.append(point - self.get_barycenter())
        self._vedo_mesh.vertices = translated_points

    def scale_to_unit_volume(self):
        # Find largest AABB dimension
        sigma = max(self.get_bounding_box_dimensions())

        # Scale uniformly by dividing
        scaled_points = []
        for point in self._vedo_mesh.vertices:
            scaled_points.append(point / sigma)
        self._vedo_mesh.vertices = scaled_points

    def get_volume(self) -> float:
        return self._vedo_mesh.volume()

    def get_faces(self):
        return self._vedo_mesh.cells

    def get_bounding_box_dimensions(self) -> list[float]:
        aabb_bounds = self._vedo_mesh.box().bounds()
        aabb_dimensions = [
            aabb_bounds[1] - aabb_bounds[0],
            aabb_bounds[3] - aabb_bounds[2],
            aabb_bounds[5] - aabb_bounds[4]
        ]

        for d in aabb_dimensions:
            if math.isnan(d):
                print('x')
                a = self._vedo_mesh.bounds()
                box = self._vedo_mesh.box()
                aabb_bounds = self._vedo_mesh.box().box().bounds()
                aabb_dimensions = [
                    aabb_bounds[1] - aabb_bounds[0],
                    aabb_bounds[3] - aabb_bounds[2],
                    aabb_bounds[5] - aabb_bounds[4]
                ]

        return aabb_dimensions

    def subdivide(self, no_iterations: int):
        vedo_copy = self._vedo_mesh.copy()
        self._vedo_mesh = vedo_copy.subdivide(no_iterations)

    def decimate(self, no_fraction: float):
        vedo_copy = self._vedo_mesh.copy()
        self._vedo_mesh = vedo_copy.decimate(no_fraction)

    def decimate_target(self, target_vertices: int):
        vedo_copy = self._vedo_mesh.copy()
        self._vedo_mesh = vedo_copy.decimate(n=target_vertices)

    def get_barycenter(self):
        return self._vedo_mesh.center_of_mass()

    def get_class(self):
        return self._class

    def get_no_vertices(self):
        return self._vedo_mesh.dataset.GetNumberOfPoints()

    def get_vertices(self):
        return self._vedo_mesh.vertices

    def get_no_cells(self):
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
        v = self.get_no_vertices()
        f = self.get_no_cells()
        t = self.get_no_triangles()
        q = self.get_no_quads()
        bb = self._vedo_mesh.box().bounds().tolist()

        return [n, c, v, f, t, q, bb]

    @property
    def path(self):
        return self._path

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


class MeshDescriptors:

    def __init__(self, p: str, n: str, cl: str, s: float, c: float, r: float, d: float, co: float, e: float):
        self._path = p
        self._name = n
        self._class = cl
        self._surface_area = s
        self._compactness = c
        self._3d_rectangularity = r
        self._diameter = d
        self._convexity = co
        self._eccentricity = e

    @property
    def name(self):
        return self._name

    def get_class(self):
        return self._class

    @property
    def surface_area(self):
        return self._surface_area

    def set_surface_area(self, s):
        self._surface_area = s

    @property
    def compactness(self):
        return self._compactness

    def set_compactness(self, c):
        self._compactness = c

    @property
    def rectangularity(self):
        return self._3d_rectangularity

    def set_rectangularity(self, r):
        self._3d_rectangularity = r

    @property
    def diameter(self):
        return self._diameter

    def set_diameter(self, d):
        self._diameter = d

    @property
    def convexity(self):
        return self._convexity

    def set_convexity(self, c):
        self._convexity = c

    @property
    def eccentricity(self):
        return self._eccentricity

    def set_eccentricity(self, e):
        self._eccentricity = e

    @property
    def path(self):
        return self._path

    def set_path(self, p):
        self._path = p
