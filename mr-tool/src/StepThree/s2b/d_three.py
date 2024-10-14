import vedo
import numpy as np
from matplotlib import pyplot as plt
import d_one as d1
import a_three as a3

def d3(m: vedo.Mesh, n: int, b: int):
    ps    = a3.sample3_n(m, n)
    areas = list(map(area, ps))
    return np.histogram(areas, bins=b)

def area(ps: np.ndarray) -> float:
    x, y, z = ps[0], ps[1], ps[2]
    a, b, c =  d1.dist(x, y), d1.dist(y, z), d1.dist(z, x)
    s       = (a + b + c) / 2
    return np.sqrt(s * (s - a) * (s - b) * (s - c))

if __name__ == "__main__":
    m = vedo.load('../../remeshed_ShapeDB/AircraftBuoyant/m1337.obj')
    plt.hist(d3, 100**3, int(100**1.5))
    plt.show()