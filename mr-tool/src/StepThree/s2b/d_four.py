import vedo
import numpy as np
from matplotlib import pyplot as plt
import d_one as d1
import a_three as a3

def d4(m: vedo.Mesh,
       n: int = int(100**3),
       b: int = int(300),
       show_hist: bool = False) -> tuple[np.ndarray, np.ndarray]:
    ps         = sample_4_n(m, n)
    vols       = d1.remove_nans(np.array([volume(p) for p in ps]))
    norm_vols  = vols / np.max(vols)
    c, bs, _   = plt.hist(norm_vols, bins=b, density=True, histtype='step')
    if show_hist: plt.show()
    return c, bs

def volume(ps: np.ndarray) -> float:
    p, q, r, s = ps[0], ps[1], ps[2], ps[3]
    a, b, c    = p - s, q - s, r - s
    vol        = np.abs(np.dot(a, np.cross(b, c))) / 6.0
    return vol

def sample_4_n(m: vedo.Mesh, n: int) -> np.ndarray:
    vs = m.vertices
    rs = np.random.choice(len(vs), size=(n, 4), replace=True)
    return np.array([vs[r] for r in rs])

if __name__ == "__main__":
    m = vedo.load('../../remeshed_ShapeDB/AircraftBuoyant/m1337.obj')
    d4(m, show_hist=True)