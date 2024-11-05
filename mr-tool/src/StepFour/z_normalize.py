import pandas as pd
import scipy.stats as S
import numpy as np

def z_score(path):
    '''Takes name of file of csv to be z-score normalized and returns new csv'''
    df = pd.read_csv('../../Output/' + path + '.csv')
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df2 = df[numeric_cols].apply(S.zscore)
    df2.to_csv('../../Output/'+path+'_z.csv')

def sort_global_des():
    '''Use this if you want to sort descriptors.csv'''
    df = pd.read_csv("../../Output/descriptors.csv")
    df.sort_values("Path", inplace=True, na_position='first')
    df.to_csv("../../Output/global_des_sorted.csv")

def fill_empty(default_val):
    '''The csvs contain empty values, fill them up with default_val'''
    df = pd.read_csv('../../Output/global_des_sorted.csv')
    df.replace('', default_val, inplace=True)
    df.fillna(default_val, inplace=True)
    df.to_csv("../../Output/gd_sorted_filled.csv")

z_score('gd')