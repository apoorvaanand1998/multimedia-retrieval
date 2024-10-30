import vedo
import numpy as np
from matplotlib import pyplot as plt
import d_one as d1
import math

def d2(m: vedo.Mesh,
       n: int = 100000,
       b: int = 300,
       show_hist: bool = False) -> tuple[np.ndarray, np.ndarray]:
    ps         = sample_2_n(m, n)
    dist2      = lambda x : d1.dist(x[0], x[1])
    ds         = d1.remove_nans(np.array([dist2(p) for p in ps]))
    norm_ds    = ds / np.max(ds)
    c, bs, _   = plt.hist(norm_ds, bins=b, density=True, histtype='step')
    if show_hist: plt.show()
    return c, bs

def sample_2_n(m: vedo.Mesh, n: int) -> np.ndarray:
    vs = m.vertices
    rs = np.random.choice(len(vs), size=(n, 2), replace=True)
    return np.array([vs[r] for r in rs])

if __name__ == "__main__":
    m = vedo.load('../../remeshed_ShapeDB/Bus/D00151.obj')
    d2(m, show_hist=True)