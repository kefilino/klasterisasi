import math
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
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
    # random_state berguna untuk memilih data random yang tetap sehingga tidak berubah tiap kali dijalankan
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
                # menjumlahkan tiap titik dari data sesuai klaster dan membagi dengan jumlah data tersebut
                centroid.at[i, j] = data[data['Klaster']==i].sum()[j]/data[data['Klaster']==i].count()[j]

    # mengembalikan nilai SSE iterasi terakhir
    return sse_new

def sse(data, centroid):
    val = 0
    # menghitung nilai sse dari semua data
    for i in range(len(data.index)):
        # menjumlahkan sse masing-masing data terhadap centroid klasternya
        val += euclidean(data.iloc[i].drop('Klaster'), centroid.iloc[data.iloc[i]['Klaster']]) ** 2
    return val

# meng-import data sheet 'Data1' dan 'Data2' menjadi variabel
data_1 = pd.read_excel('Data.xlsx', sheet_name='Data1').drop('No', axis=1)
data_2 = pd.read_excel('Data.xlsx', sheet_name='Data2').drop('No', axis=1)

# inisialisasi list kosong
t = list()
s = list()

# iterasi untuk k=1 sampai k=5
for i in range(50):
    # menambahkan nilai index k=i kedalam list t
    t.append(i+1)
    # menambahkan nilai sse tiap k=i kedalam list s
    s.append(k_means(data_1, i+1, 10))

# membuat plot menggunakan library matplotlib untuk visualisasi grafik korelasi antara nilai k dengan sse
plt.plot(s, t)
plt.xlim(left=300000, right=0)
plt.yticks(np.arange(1, len(t)+1, 1))
plt.xlabel('SSE (lebih kecil lebih baik)')
plt.ylabel('Jumlah Klaster (K)')
plt.title('Korelasi antara jumlah klaster (K) dengan nilai SSE')
plt.show()