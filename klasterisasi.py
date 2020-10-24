import math;
import pandas as pd;

# fungsi euclidean untuk menghitung jarak antar titik
def euclidean(x, y):
    # kondisi ketika titik x dan y hanya berupa skalar
    if isinstance(x, (int, float)) and isinstance(y, (int, float)):
        return math.sqrt((x - y) ** 2)

    # kondisi ketika titik x dan y memiliki banyak dimensi
    dist = 0
    for i in range(x.size):
        dist += (x[i] - y[i]) ** 2
    return math.sqrt(dist)

# fungsi k-means clustering dengan parameter banyaknya k dan iterasi maks
def k_means(data, k=1, max_it=10):
    # mengambil titik dari data sebanyak k secara random sebagai centroid awal
    centroid = data.sample(n=k, random_state=1).reset_index(drop=True)
    
    for it in range(max_it):
        cluster = []
        for i in range(len(data.index)):
            min_idx = 0
            for j in range(k):
                dist = euclidean(centroid.iloc[j], data.iloc[i])
                if j == 0:
                    min_val = dist
                
                if dist < min_val:
                    min_idx = j
                    min_val = dist
            cluster.append(min_idx)

        data['Klaster'] = cluster
        for i in range(k):
            for j in centroid.columns:
                centroid.at[i, j] = data[data['Klaster']==i].sum()[j]/data[data['Klaster']==i].count()[j]
        print(sse(data, centroid))
    
    return sse(data, centroid)

def sse(data, centroid):
    val = 0
    for i in range(len(data.index)):
        val += euclidean(data.iloc[i].drop('Klaster'), centroid.iloc[data.iloc[i]['Klaster']]) ** 2
    return val

data_1 = pd.read_excel('Data.xlsx', sheet_name='Data1').drop('No', axis=1)
data_2 = pd.read_excel('Data.xlsx', sheet_name='Data2').drop('No', axis=1)

k_means(data_1, 50, 10)