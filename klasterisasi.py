import math
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

# fungsi euclidean untuk menghitung jarak antar titik
def euclidean(x, y):
    # kondisi ketika titik x dan y hanya berupa skalar
    if isinstance(x, (int, float)) and isinstance(y, (int, float)):
        return math.sqrt((x - y) ** 2)

    # kondisi ketika titik x dan y memiliki banyak dimensi
    dist = 0
    for i in range(x.size):
        dist += pow((x[i] - y[i]), 2)
    return math.sqrt(dist)

# fungsi k-means clustering dengan parameter banyaknya k dan iterasi maks
def k_means(data, k=1, max_it=10):
    # mengambil titik dari data sebanyak k secara random tetap sebagai centroid awal
    centroid = data.sample(n=k, random_state=0).reset_index(drop=True)
    sse_new, sse_old = 0, 0
    
    # melakukan klastering sebanyak max_it
    for it in range(max_it):
        cluster = []
        
        # melakukan klastering terhadap setiap titik pada iterasi ke-it
        for i in range(len(data.index)):
            min_idx = 0
            # hitung jarak dari data ke-i dengan setiap centroid untuk klasterisasi
            for j in range(k):
                # menghitung jarak data terhadap centroid ke-j menggunakan rumus euclidean
                dist = euclidean(centroid.iloc[j], data.iloc[i])
                
                # inisialisasi jarak minimum
                if j == 0:
                    min_val = dist
                
                # menemukan jarak minimum dari jarak titik i terhadap centroid
                if dist < min_val:
                    min_idx = j
                    min_val = dist
                  
            # menambahkan klaster kedalam list index ke-i
            cluster.append(min_idx)

        # menambahkan kolom klaster kedalam data
        data['Klaster'] = cluster
        # menyimpan data sse lama dan menghitung data sse baru
        sse_old = sse_new
        sse_new = sse(data, centroid)
        
        # jika nilai sse tidak berubah maka hentikan iterasi
        if sse_new == sse_old:
            break
        
        # menghitung centroid baru
        for i in range(k):
            for j in centroid.columns:
                centroid.at[i, j] = data[data['Klaster']==i].sum()[j]/data[data['Klaster']==i].count()[j]

    return sse_new

def sse(data, centroid):
    val = 0
    for i in range(len(data.index)):
        val += euclidean(data.iloc[i].drop('Klaster'), centroid.iloc[data.iloc[i]['Klaster']]) ** 2
    return val

data_1 = pd.read_excel('Data.xlsx', sheet_name='Data1').drop('No', axis=1)
data_2 = pd.read_excel('Data.xlsx', sheet_name='Data2').drop('No', axis=1)

k_means(data_1, 5, 10)