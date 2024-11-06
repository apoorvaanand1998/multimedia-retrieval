import Mesh as M
import pathlib as P

ground_truth_path = P.Path('../../FINAL_remeshed_repaired_normalized_ShapeDB/')

def which_method(mthd, c_mesh):
    match mthd:
        case 'euc':
            pass
        case 'hnsw':
            pass
    return df

def df_to_meshes(df, k):
    df             = df.head(k)
    f              = lambda x : ground_truth_path + x + '.obj'
    df['fullpath'] = df['name'].apply(f)