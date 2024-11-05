import read_csv as R
import pathlib as p
import pandas as pd

from_path   = p.Path('../../FINAL_remeshed_repaired_normalized_ShapeDB/')
all_classes = [f for f in from_path.iterdir()]
all_meshes2 = list(map(lambda x : [m for m in x.iterdir()], all_classes))
all_meshes  = [x for xs in all_meshes2 for x in xs]


