import scipy.spatial.distance as SD
import pandas as pd

def find_dist(input_mesh):
    '''takes input_mesh in the form class_name/mesh'''
    df  = pd.read_csv('../../Output/matrix.csv')
    r   = df.loc[df['name'] == input_mesh]

    df2         = pd.DataFrame()
    df2['name'] = df['name']

    df = df.drop(df.columns[[0, 1]], axis=1)
    r  = r.drop(r.columns[[0, 1]], axis=1)
    df = df.transpose()
    r  = r.transpose()
    #r  = r.drop(r.columns[[0]], axis=1)
    r  = r.to_numpy().flatten()

    dist_r         = lambda x : SD.euclidean(r, x.to_numpy())
                    ## no feature or distance weighing done
    dist2          = pd.DataFrame()
    dist2['dist']  = df.apply(dist_r, axis=0)
    
    df  = df.transpose()
    res = pd.concat([df2, df, dist2], axis=1)
    
    res.sort_values('dist', inplace=True, na_position='first')
    return res

if __name__ == '__main__':
    print(find_dist('Bicycle/D00016'))