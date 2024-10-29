import csv
import numpy as np
import ast

def row_to_hb(row: str) -> tuple[np.ndarray, np.ndarray]:
    h = row[1]
    h = h.replace("\n", "")
    h = h.replace(" ", "")
    h = h[7:]
    h = h.split("array(")
    h0 = h[0][:-2]
    h1 = h[1][:-2]
    h0 = np.fromstring(h0)
    h1 = np.fromstring(h1)
    return h0, h1

def pick_row(c_mesh : str)