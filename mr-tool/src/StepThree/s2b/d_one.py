import vedo
import numpy as np
from matplotlib import pyplot as plt

def d_one(m: vedo.Mesh, n: int, b: int):
    barycenter = m.center_of_mass()
    vs         = m.vertices
    ri         = np.random.choice(len(vs), size=n, replace=True)
    vr         = vs[ri]
    dists      = np.array(list(map(lambda y : dist(barycenter, y), vr)))
    c, b_edges = np.histogram(dists, bins=b)
    normalized = c / np.sum(c)
    return normalized, b_edges

def dist(x: np.ndarray, y: np.ndarray) -> np.float64:
    return np.linalg.norm(x - y)

if __name__ == "__main__":
    m = vedo.load('../../remeshed_ShapeDB/AircraftBuoyant/m1337.obj')
    plt.hist(d_one(m, 100**3, int(100**1.5)))
    plt.show()