import math

import vedo
import numpy as np
from matplotlib import pyplot as plt


#################### A3 ####################
def a3(m: vedo.Mesh,
       n: int = int(100 ** 3),
       b: int = int(100 ** 1.5),
       show_hist: bool = False) -> tuple[np.ndarray, np.ndarray]:
    raw_angles = np.array(angles(sample_3_n(m, n)))
    norm_angs = raw_angles / np.max(raw_angles)
    c, bs, _ = plt.hist(norm_angs, bins=b, density=True, histtype='step')
    if show_hist: plt.show()
    return c, bs


def angles(ps: np.ndarray) -> np.ndarray:
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


#################### END A3 ####################

#################### D1 #####################
def d1(m: vedo.Mesh,
       n: int = 10000,
       b: int = 100,
       show_hist=False) -> tuple[np.ndarray, np.ndarray]:
    barycenter = m.center_of_mass()
    vs = m.vertices
    ri = np.random.choice(len(vs), size=n, replace=True)
    vr = vs[ri]
    distB = lambda v: dist(barycenter, v)
    dists = remove_nans(np.array([distB(v) for v in vr]))
    norm_ds = dists / np.max(dists)
    c, bs, _ = plt.hist(norm_ds, bins=b, density=True, histtype='step')
    if show_hist: plt.show()
    return c, bs


def dist(x: np.ndarray, y: np.ndarray) -> np.float64:
    return np.linalg.norm(x - y)


def remove_nans(x: np.ndarray) -> np.ndarray:
    return x[~np.isnan(x)]


#################### END D1 #####################

#################### D2 #####################
def d2(m: vedo.Mesh,
       n: int = 100000,
       b: int = int(math.sqrt(100000)),
       show_hist: bool = False) -> tuple[np.ndarray, np.ndarray]:
    ps = sample_2_n(m, n)
    dist2 = lambda x: dist(x[0], x[1])
    ds = remove_nans(np.array([dist2(p) for p in ps]))
    norm_ds = ds / np.max(ds)
    c, bs, _ = plt.hist(norm_ds, bins=b, density=True, histtype='step')
    if show_hist: plt.show()
    return c, bs


def sample_2_n(m: vedo.Mesh, n: int) -> np.ndarray:
    vs = m.vertices
    rs = np.random.choice(len(vs), size=(n, 2), replace=True)
    return np.array([vs[r] for r in rs])


#################### END D2 #####################


#################### D3 #####################
def d3(m: vedo.Mesh,
       n: int = int(100 ** 3),
       b: int = int(100 ** 1.5),
       show_hist: bool = False) -> tuple[np.ndarray, np.ndarray]:
    ps = sample_3_n(m, n)
    areas = remove_nans(np.array([area(p) for p in ps]))
    norm_areas = areas / np.max(areas)
    c, bs, _ = plt.hist(norm_areas, bins=b, density=True, histtype='step')
    if show_hist: plt.show()
    return c, bs


def area(ps: np.ndarray) -> float:
    x, y, z = ps[0], ps[1], ps[2]
    a, b, c = dist(x, y), dist(y, z), dist(z, x)
    s = (a + b + c) / 2
    return np.sqrt(s * (s - a) * (s - b) * (s - c))


#################### END D3 #####################


#################### D4 #####################
def d4(m: vedo.Mesh,
       n: int = int(100 ** 3),
       b: int = int(100 ** 1.5),
       show_hist: bool = False) -> tuple[np.ndarray, np.ndarray]:
    ps = sample_4_n(m, n)
    vols = remove_nans(np.array([volume(p) for p in ps]))
    norm_vols = vols / np.max(vols)
    c, bs, _ = plt.hist(norm_vols, bins=b, density=True, histtype='step')
    if show_hist: plt.show()
    return c, bs


def volume(ps: np.ndarray) -> float:
    p, q, r, s = ps[0], ps[1], ps[2], ps[3]
    a, b, c = p - s, q - s, r - s
    vol = np.abs(np.dot(a, np.cross(b, c))) / 6.0
    return vol


def sample_4_n(m: vedo.Mesh, n: int) -> np.ndarray:
    vs = m.vertices
    rs = np.random.choice(len(vs), size=(n, 4), replace=True)
    return np.array([vs[r] for r in rs])
#################### END D4 #####################
