import pandas as pd
from scipy.spatial.distance import squareform, pdist

def agnes(data, max_level=1, method='single'):
    print(data)
    #print(pd.DataFrame(squareform(pdist(data.iloc[:, :])), columns=data.index, index=data.index))

data_2 = pd.read_excel('Data.xlsx', sheet_name='Data2').drop('No', axis=1)

agnes(data_2, 4, 'single')