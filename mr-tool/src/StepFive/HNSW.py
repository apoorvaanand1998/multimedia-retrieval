import hnswlib
import numpy as np
import pandas as pd


def build_hnsw_graph(feature_vectors: np.ndarray) -> hnswlib.Index:

    assert feature_vectors.dtype == 'float64'

    dim = feature_vectors.shape[1]
    hnsw_index = hnswlib.Index(space='l2', dim=dim)

    hnsw_index.init_index(max_elements=feature_vectors.shape[0], ef_construction=300, M=32)
    hnsw_index.add_items(feature_vectors)

    return hnsw_index

def query_hnsw(index: hnswlib.Index, query_vector: np.ndarray, k: int) -> tuple[np.ndarray, np.ndarray]:
    assert query_vector.shape[0] == index.dim

    indices, dist = index.knn_query(query_vector, k=k)
    unpacked_indices, unpacked_dist = indices[0], dist[0]

    return unpacked_indices, unpacked_dist

def toy_query(input_c_mesh):
    df  = pd.read_csv('../../Output/matrix.csv')
    q   = df.loc[df['name'] == input_c_mesh]
    q   = q.drop(q.columns[[0, 1]], axis=1)
    q   = q.to_numpy().flatten()
    return q

def g():
    data = pd.read_csv('../../Output/matrix.csv')
    numd = data.drop(columns=['name', 'id']).values
    return build_hnsw_graph(numd)

def df(input_c_mesh, g : hnswlib.Index):
    rows, dists              = query_hnsw(g, toy_query(input_c_mesh), 2483)
    df                       = pd.read_csv('../../Output/matrix.csv')
    df.loc[rows, 'dist'] = dists
    df.sort_values('dist', inplace=True, na_position='first')
    return df

if __name__ == '__main__':
    g = g()
    print(df('Bed/D00121', g))