import hnswlib
import numpy as np


def build_hnsw_graph(feature_vectors: np.ndarray) -> hnswlib.Index:
    dim = feature_vectors.shape[1]
    hnsw_index = hnswlib.Index(space='l2', dim=dim)

    hnsw_index.init_index(max_elements=feature_vectors.shape[0], ef_construction=300, M=32)
    hnsw_index.add_items(feature_vectors)

    return hnsw_index


def query_hnsw(index: hnswlib.Index, query_vector: np.ndarray, k: int) -> tuple[np.ndarray, np.ndarray]:
    assert query_vector.shape[1] == index.dim

    indices, dist = index.knn_query(query_vector, k=k)

    return indices, dist

if __name__ == '__main__':
    toy_data = np.random.random((100, 1000)).astype('float32')
    hnsw = build_hnsw_graph(toy_data)

    toy_query = np.random.random((1, 1000)).astype('float32')
    neighbor_indices, distances = query_hnsw(hnsw, toy_query, 5)

    resulting_shapes = toy_data[neighbor_indices] # still index to path of shape

    print(resulting_shapes)