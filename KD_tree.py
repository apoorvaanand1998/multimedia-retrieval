import numpy as np
from sklearn.neighbors import KDTree

def build_kd_tree(X: np.ndarray) -> KDTree:
    return KDTree(X, leaf_size=20, metric='minowski')

def query_kd_tree(kd_tree: KDTree, X: np.ndarray, k: int) -> tuple[np.ndarray, np.ndarray]:
    distances, neighbor_indices = kd_tree.query(X, k)

    return distances, neighbor_indices

if __name__ == '__main__':
    shape_features = np.random.rand(100, 3)
    kd_tree = build_kd_tree(shape_features)
    distances, neighbor_indices = query_kd_tree(kd_tree, shape_features, 5)

    shape_paths = shape_features[neighbor_indices] # still index to path of shape