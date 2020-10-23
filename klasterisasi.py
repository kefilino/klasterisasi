import math;
import pandas as pd;

def euclidean(x, y):
    if isinstance(x, (int, float)) and isinstance(y, (int, float)):
        return math.sqrt((x - y) ** 2)

    dist = 0
    for i in range(x.size):
        dist += (x[i] - y[i]) ** 2
    return math.sqrt(dist)

data_1 = pd.read_excel('Data.xlsx', sheet_name='Data1')
data_2 = pd.read_excel('Data.xlsx', sheet_name='Data2')