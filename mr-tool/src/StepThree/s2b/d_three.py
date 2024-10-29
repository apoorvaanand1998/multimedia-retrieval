import vedo
import numpy as np
from matplotlib import pyplot as plt
import d_one as d1
import a_three as a3

def d3(m: vedo.Mesh,
       n: int = int(100**3),
       b: int = int(300),
       show_hist: bool = False) -> tuple[np.ndarray, np.ndarray]:
    ps         = a3.sample_3_n(m, n)
    areas      = d1.remove_nans(np.array([area(p) for p in ps]))
    norm_areas = areas / np.max(areas)
    c, bs, _   = plt.hist(norm_areas, bins=b, density=True, histtype='step')
    if show_hist: plt.show()
    return c, bs

def area(ps: np.ndarray) -> float:
    x, y, z = ps[0], ps[1], ps[2]
    a, b, c =  d1.dist(x, y), d1.dist(y, z), d1.dist(z, x)
    s       = (a + b + c) / 2
    return np.sqrt(s * (s - a) * (s - b) * (s - c))

if __name__ == "__main__":
    m = vedo.load('../../remeshed_ShapeDB/AircraftBuoyant/m1337.obj')
    d3(m, show_hist=True)   