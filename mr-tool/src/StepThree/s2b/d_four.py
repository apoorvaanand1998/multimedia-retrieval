import vedo
import numpy as np
from matplotlib import pyplot as plt
import d_one as d1
import a_three as a3

def d4(m: vedo.Mesh, n: int, b: int):
    ps         = sample4_n(m, n)
    vols       = list(map(volume, ps))
    c, b_edges = np.histogram(vols, bins=b)
    normalized = c / np.sum(c)
    return normalized, b_edges

def volume(ps: np.ndarray) -> float:
    p, q, r, s = ps[0], ps[1], ps[2], ps[3]
    a, b, c    = p - s, q - s, r - s
    vol        = np.abs(np.dot(a, np.cross(b, c))) / 6.0
    return vol

def sample4_n(m: vedo.Mesh, n: int) -> list[np.ndarray]:
    r3s = []
    for i in range(n):
        rs = sample4(m)
        r3s.append(rs)
    return r3s

def sample4(m: vedo.Mesh) -> np.ndarray:
    vs = m.vertices
    ri = np.random.choice(len(vs), size=4, replace=False)
    rs = vs[ri]
    return rs