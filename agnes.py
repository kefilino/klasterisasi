# Nama  : Kefilino Khalifa Filardi
#       : Aithra Junia Bouty		
# NPM   : 140810180028
#       : 140810180054
# Kelas : B
# Desc  : Program untuk klasterisasi menggunakan algoritma AGNES dan mencari hasil klasterisasi serta visualisasinya.

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
# library dendogram dan linkage hanya untuk visualisasi
from scipy.cluster.hierarchy import dendrogram, linkage

# fungsi mencari jarak titik x dan y menggunakan rumus manhattan
def manhattan(x, y):
    # kondisi ketika titik x dan y hanya berupa skalar
    if isinstance(x, (int, float)) and isinstance(y, (int, float)):
        return abs(x - y)

    # kondisi ketika titik x dan y memiliki banyak dimensi
    dist = 0
    for i in range(len(x)):
        dist += abs(x[i] - y[i])
    return dist

# menghitung matrix jarak antar titik pada data
def dist_matrix(data):
    dm = []
    # untuk setiap data akan dihitung jaraknya
    for i in range(len(data)):
        l = []
        for j in range(len(data)):
            dist = manhattan(data[i][0], data[j][0])
            # hasil menyesuaikan index dan disimpan di list sementara
            l.append(dist)
        # list utama ditambah ketika perhitungan satu titik terhadap seluruh titik lainnya selesai
        dm.append(l)
    return dm

def agnes(data, max_level=1, method='single'):
    # mengubah data DataFrame menjadi multi dimensional list agar mudah diubah
    data_matrix = [[i] for i in range(data.to_numpy().shape[0])]
    # membuat list baru untuk menyimpan data sample yang akan digunakan untuk menyimpan klaster baru
    sample = [[list(data.to_numpy()[i])] for i in range(data.to_numpy().shape[0])]
    # menghitung jumlah data dalam sample awal
    m = len(sample)
    i = 1
    
    while m > 1:
        # membuat array distance matrix
        dm = np.array(dist_matrix(sample))
        # mencari array dengan nilai minimum atau jarak terdekat
        min_dist = np.where(dm == dm.min())[0]
        # memindahkan list titik ke-2 minimum tadi kedalam list titik ke-1
        value_to_add = sample.pop(min_dist[1])
        sample[min_dist[0]].append(value_to_add)

        # mendapatkan titik dengan
        print('Titik dengan jarak terdekat (MIN(Dman)) : \n', data_matrix[min_dist[0]], 'dan', data_matrix[min_dist[1]])

        data_matrix[min_dist[0]].append(data_matrix[min_dist[1]])
        data_matrix[min_dist[0]] = [data_matrix[min_dist[0]]]
        v = data_matrix.pop(min_dist[1])
        # menyimpan jumlah data baru sample
        m = len(sample)

        # mencetak data, klaster, dan ukuran data yang baru terbentuk
        print('\nData Iterasi ke-%i : \n' % i, data_matrix)
        print('\nKlaster baru yang terbuat\t: ', data_matrix[min_dist[0]])
        print('Ukuran data setelah klastering\t: ', m)
        print('\n')
        i+=1
    

def dendogram_agnes(data):
    # membuat visualisasi dendrogram AGNES dengan level = 4
    dn = linkage(data.to_numpy(), 'single')
    plt.figure()
    plt.xlabel('Index Data')
    plt.ylabel('Jarak')
    plt.title('Visualisasi Agglomerative Hierarchical Clustering')
    dendrogram(dn, p=4, truncate_mode='level')
    plt.show()

# meng-import sheet 'Data2' dari file 'Data.xlsx' menggunakan library pandas
data_2 = pd.read_excel('Data.xlsx', sheet_name='Data2').drop('No', axis=1)

dendogram_agnes(data_2)
agnes(data_2, 4, 'single')