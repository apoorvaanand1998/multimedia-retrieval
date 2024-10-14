import vedo
import numpy as np
from matplotlib import pyplot as plt
import d_one as d1

def d2(m: vedo.Mesh, n: int, b: int):
    ps         = sample2_n(m, n)
    ds         = list(map(lambda x : d1.dist(x[0], x[1]), ps))
    c, b_edges = np.histogram(ds, bins=b)
    normalized = c / np.sum(c)
    return normalized, b_edges

def sample2_n(m: vedo.Mesh, n: int) -> list[np.ndarray]:
    """Sample 2 points from m, n times"""
    r3s = []
    for i in range(n):
        rs = sample2(m)
        r3s.append(rs)
    return r3s

def sample2(m: vedo.Mesh) -> np.ndarray:
    vs = m.vertices
    ri = np.random.choice(len(vs), size=2, replace=False)
    rs = vs[ri]
    return rs