import read_csv as R
import pathlib as p
import pandas as pd
import expand_hist_df as E

from_path   = p.Path('../../FINAL_remeshed_repaired_normalized_ShapeDB/')
all_classes = [f for f in from_path.iterdir()]
all_meshes2 = list(map(lambda x : [m for m in x.iterdir()], all_classes))
all_meshes1 = [x for xs in all_meshes2 for x in xs]
all_meshes  = [x.parent.name + '/' + x.with_suffix('').name for x in all_meshes1]
all_meshes  = sorted(all_meshes)

df        = pd.DataFrame({'name': all_meshes})
df2       = pd.read_csv('../../Output/gd_z.csv')
df2       = df2.drop(df2.columns[[0]], axis=1)
df3       = pd.concat([df, df2], axis=1)
f_a3      = lambda x : R.get_vec('a3', x)
f_d1      = lambda x : R.get_vec('d1', x)
f_d2      = lambda x : R.get_vec('d2', x)
f_d3      = lambda x : R.get_vec('d3', x)
f_d4      = lambda x : R.get_vec('d4', x)

df4       = pd.DataFrame()
df4['a3'] = df3['name'].apply(f_a3)
df4['d1'] = df3['name'].apply(f_d1)
df4['d2'] = df3['name'].apply(f_d2)
df4['d3'] = df3['name'].apply(f_d3)
df4['d4'] = df3['name'].apply(f_d4)

df5       = E.expand(df4)
df6       = pd.concat([df3, df5], axis=1)
print(df6)
df6.to_csv('../../Output/matrix.csv')