import vedo
import numpy as np
from matplotlib import pyplot as plt

def d_one(m: vedo.Mesh,
          n: int=10000,
          b: int=100,
          show_hist=False) -> tuple[np.ndarray, np.ndarray]:
    barycenter = m.center_of_mass()
    vs         = m.vertices
    ri         = np.random.choice(len(vs), size=n, replace=True)
    vr         = vs[ri]
    distB      = lambda v : dist(barycenter, v)
    dists      = remove_nans(np.array([distB(v) for v in vr]))
    norm_ds    = dists / np.max(dists)
    c, bs, _   = plt.hist(norm_ds, bins=b, density=True, histtype='step')
    if show_hist: plt.show()
    return c, bs

def dist(x: np.ndarray, y: np.ndarray) -> np.float64:
    return np.linalg.norm(x - y)

def remove_nans(x: np.ndarray) -> np.ndarray:
    return x[~np.isnan(x)]

if __name__ == "__main__":
    m = vedo.load('../../remeshed_ShapeDB/AircraftBuoyant/m1337.obj')
    d_one(m, show_hist=True)