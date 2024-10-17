import vedo
import numpy as np
from matplotlib import pyplot as plt

def a3(m: vedo.Mesh,
       n: int = int(100**3),
       b: int = int(100**1.5),
       show_hist: bool = False) -> tuple[np.ndarray, np.ndarray]:
    raw_angles = np.array(angles(sample_3_n(m, n)))
    norm_angs  = raw_angles / np.max(raw_angles)
    c, bs, _   = plt.hist(norm_angs, bins=b, density=True, histtype='step')
    if show_hist: plt.show()
    return c, bs
    
def angles(ps : np.ndarray) -> np.ndarray:
    r = np.array([angle(p) for p in ps])
    return r[~np.isnan(r)]

def angle(p: np.ndarray) -> int:
    """Pass 3 points A, B, C in array, get angle between AB and BC in degrees"""
    a, b, c = p[0], p[1], p[2]
    ab, bc = a - b, b - c

    dot = np.dot(ab, bc)
    mag_ab = np.linalg.norm(ab)
    mag_bc = np.linalg.norm(bc)

    cos_angle = dot / (mag_ab * mag_bc)
    return np.degrees(np.arccos(cos_angle))

def sample_3_n(m: vedo.Mesh, n: int) -> np.ndarray:
    vs = m.vertices
    rs = np.random.choice(len(vs), size=(n, 3), replace=True)
    return np.array([vs[r] for r in rs])

if __name__ == "__main__":
    m = vedo.load('../../remeshed_ShapeDB/AircraftBuoyant/m1337.obj')
    a3(m, show_hist=True)