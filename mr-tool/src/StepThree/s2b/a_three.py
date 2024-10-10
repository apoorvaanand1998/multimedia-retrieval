import vedo
import numpy as np
from matplotlib import pyplot as plt

def a3(m: vedo.Mesh, n: int, b: int):
    raw_angles = np.array(angles(sample3_n(m, n)))
    return np.histogram(raw_angles, bins=b)

def angles(ps : list[np.ndarray]) -> list[int]:
    return list(map(angle, ps))

def angle(p: np.ndarray) -> int:
    """Pass 3 points A, B, C in array, get angle between AB and BC in degrees"""
    a, b, c = p[0], p[1], p[2]
    ab, bc = a - b, b - c

    dot = np.dot(ab, bc)
    mag_ab = np.linalg.norm(ab)
    mag_bc = np.linalg.norm(bc)

    cos_angle = dot / (mag_ab * mag_bc)
    return np.degrees(np.arccos(cos_angle))

def sample3_n(m: vedo.Mesh, n: int) -> list[np.ndarray]:
    """Sample 3 points from m, n times"""
    r3s = []
    for i in range(n):
        rs = sample3(m)
        r3s.append(rs)
    return r3s

def sample3(m: vedo.Mesh) -> np.ndarray:
    vs = m.vertices
    ri = np.random.choice(len(vs), size=3, replace=False)
    rs = vs[ri]
    return rs

if __name__ == "__main__":
    m = vedo.load('../../remeshed_ShapeDB/AircraftBuoyant/m1337.obj')
    plt.hist(a3(m, 100**2, 100))
    plt.show()