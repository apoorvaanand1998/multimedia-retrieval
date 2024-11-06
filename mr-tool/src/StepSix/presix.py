import Mesh as M
import pathlib as P
import StepFour.dist as S4
import StepFive.HNSW as S5

ground_truth_path = P.Path('../../FINAL_remeshed_repaired_normalized_ShapeDB/')

def which_method(mthd, c_mesh):
    match mthd:
        case 'euc':
            return S4.find_dist(c_mesh)
        case 'hnsw':
            g = S5.g()
            return S5.df(c_mesh, g)

def df_to_meshes(df, k):
    f              = lambda x : str(ground_truth_path) + '/' + x + '.obj'
    df['fullpath'] = df['name'].apply(f)
    # print(df)
    df  = df.head(k)
    np1 = df['fullpath'].to_numpy()
    np2 = df['dist'].to_numpy()
    l1  = [M.Mesh(x) for x in np1]
    f   = lambda x : 1 / (x+1)
    l2  = [f(x) for x in np2]
    return l1, l2

# print(df_to_meshes(which_method('euc', 'Bed/D00121'), 10))
# print(df_to_meshes(which_method('hnsw', 'Bed/D00121'), 10))