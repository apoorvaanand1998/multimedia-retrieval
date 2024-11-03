import numpy as np
import utils
from scipy import stats

from Mesh import MeshDescriptors

ORIGINAL_DB = "remeshed_normalized_filled_ShapeDB_united"
OUTPUT_DB = "remeshed_normalized_filled_ShapeDB_united_normalized"


def normalize_one(desc: MeshDescriptors) -> MeshDescriptors:
    array = np.array(
        [desc.surface_area, desc.compactness, desc.convexity, desc.rectangularity, desc.eccentricity, desc.diameter])
    array = np.array([np.nan if x is None or np.isinf(x) else x for x in array])

    array = stats.zscore(array)

    array = [None if np.isnan(x) else x for x in array]

    desc.set_surface_area(array[0])
    desc.set_convexity(array[1])
    desc.set_compactness(array[2])
    desc.set_rectangularity(array[3])
    desc.set_eccentricity(array[4])
    desc.set_diameter(array[5])

    return desc


def normalize(desc: list[MeshDescriptors]) -> np.array:
    surface_areas = []
    convexities = []
    compactness = []
    rectangularities = []
    eccentrities = []
    diameters = []

    for d in desc:
        surface_areas.append(d.surface_area)
        convexities.append(d.convexity)
        compactness.append(d.compactness)
        rectangularities.append(d.rectangularity)
        eccentrities.append(d.eccentricity)
        diameters.append(d.diameter)

    surface_areas = np.array([np.nan if x is None or np.isinf(x) else x for x in surface_areas])
    convexities = np.array([np.nan if x is None or np.isinf(x) else x for x in convexities])
    compactness = np.array([np.nan if x is None or np.isinf(x) else x for x in compactness])
    rectangularities = np.array([np.nan if x is None or np.isinf(x) else x for x in rectangularities])
    eccentrities = np.array([np.nan if x is None or np.isinf(x) else x for x in eccentrities])
    diameters = np.array([np.nan if x is None or np.isinf(x) else x for x in diameters])

    surface_areas = stats.zscore(surface_areas, nan_policy='omit')
    convexities = stats.zscore(convexities, nan_policy='omit')
    compactness = stats.zscore(compactness, nan_policy='omit')
    rectangularities = stats.zscore(rectangularities, nan_policy='omit')
    eccentrities = stats.zscore(eccentrities, nan_policy='omit')
    diameters = stats.zscore(diameters, nan_policy='omit')

    surface_areas = [None if np.isnan(x) else x for x in surface_areas]
    convexities = [None if np.isnan(x) else x for x in convexities]
    compactness = [None if np.isnan(x) else x for x in compactness]
    rectangularities = [None if np.isnan(x) else x for x in rectangularities]
    eccentrities = [None if np.isnan(x) else x for x in eccentrities]
    diameters = [None if np.isnan(x) else x for x in diameters]

    for idx, d in enumerate(desc):
        print(f"{idx + 1}/{len(desc)}")
        d.set_surface_area(surface_areas[idx])
        d.set_convexity(convexities[idx])
        d.set_compactness(compactness[idx])
        d.set_rectangularity(rectangularities[idx])
        d.set_eccentricity(eccentrities[idx])
        d.set_diameter(diameters[idx])

    return desc

# def main():
#     desc = utils.get_output_descriptors(ORIGINAL_DB)
#     utils.save_output_descriptors(OUTPUT_DB, normalize(desc))
#
#
# main()
