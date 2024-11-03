import numpy as np

import heapq

import utils
from enum import Enum

from Mesh import Mesh, MeshDescriptors

DATABASE_TO_QUERY = "remeshed_normalized_filled_ShapeDB"
ALL_SHAPES: list[MeshDescriptors] = utils.get_output_descriptors(DATABASE_TO_QUERY + "_united")


class QueryMode(Enum):
    EUCLIDEAN = "euclidean",
    EMD = "emd"


class QueryResult:

    def __init__(self, mesh_descriptors: MeshDescriptors, dist: float):
        self.mesh_descriptors = mesh_descriptors
        self.dist = dist


def get_feature_vector(mesh_descriptors: MeshDescriptors) -> np.ndarray:
    global_desc = np.array(
        [mesh_descriptors.surface_area, mesh_descriptors.compactness, mesh_descriptors.rectangularity,
         mesh_descriptors.diameter, mesh_descriptors.convexity, mesh_descriptors.eccentricity])
    all_desc = np.concatenate(
        (global_desc, mesh_descriptors.a3, mesh_descriptors.d1, mesh_descriptors.d2, mesh_descriptors.d3,
         mesh_descriptors.d4)
    )
    return all_desc


def get_feature_vector_tuple(mesh_descriptors: MeshDescriptors) -> np.ndarray:
    global_desc = np.array(
        [mesh_descriptors.surface_area, mesh_descriptors.compactness, mesh_descriptors.rectangularity,
         mesh_descriptors.diameter, mesh_descriptors.convexity, mesh_descriptors.eccentricity])
    all_desc = np.concatenate(
        (global_desc, mesh_descriptors.a3[0], mesh_descriptors.d1[0], mesh_descriptors.d2[0], mesh_descriptors.d3[0],
         mesh_descriptors.d4[0])
    )
    return all_desc


def query(mesh_descriptors: MeshDescriptors, no_results: int = 5, mode: QueryMode = QueryMode.EUCLIDEAN) -> (
        tuple)[list[QueryResult], int, int]:
    query_mesh_fv = get_feature_vector_tuple(mesh_descriptors)  # Query Mesh feature vector

    results: list[QueryResult] = []
    no_skipped = 0
    for shape in ALL_SHAPES:
        shape_fv = get_feature_vector(shape)

        if mode == QueryMode.EUCLIDEAN:
            try:
                dist = np.linalg.norm(query_mesh_fv - shape_fv)
                results.append(QueryResult(shape, dist))
            except TypeError:
                print('Skipping comparison with shape [None values]' + shape.path)
                no_skipped += 1
            except ValueError:
                print('Skipping comparison with shape [Vectors diff size]' + shape.path)
                print('Query mesh feature vector: ' + str(query_mesh_fv.shape))
                print('Current mesh feature vector: ' + str(shape_fv.shape))
                no_skipped += 1
        if mode == QueryMode.EMD:
            print('EMD')

    return heapq.nsmallest(no_results, results, key=lambda x: x.dist), len(results), no_skipped
