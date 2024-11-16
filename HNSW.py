import hnswlib
import numpy as np
import pandas as pd


def build_hnsw_graph(feature_vectors: np.ndarray) -> hnswlib.Index:

    assert feature_vectors.dtype == 'float64'

    dim = feature_vectors.shape[1]
    hnsw_index = hnswlib.Index(space='l2', dim=dim)

    hnsw_index.init_index(max_elements=feature_vectors.shape[0], ef_construction=500, M=64)
    hnsw_index.add_items(feature_vectors)

    return hnsw_index


def query_hnsw(index: hnswlib.Index, query_vector: np.ndarray, k: int) -> tuple[np.ndarray, np.ndarray]:
    assert query_vector.shape[0] == index.dim

    indices, dist = index.knn_query(query_vector, k=k)
    unpacked_indices, unpacked_dist = indices[0], dist[0]

    return unpacked_indices, unpacked_dist


if __name__ == '__main__':
    data = pd.read_csv('USE_THIS_MATRIX.csv')
    path_data = data['name'].values
    data_numeric: np.ndarray = data.drop(columns=['name', 'id']).values
    hnsw = build_hnsw_graph(data_numeric)

    toy_query = data_numeric[70]
    neighbor_indices, distances = query_hnsw(hnsw, toy_query, 5)

    resulting_shapes = path_data[neighbor_indices]

    path_and_distances_dict = {path: distance for path, distance in zip(resulting_shapes, distances)}
    print(path_and_distances_dict)



