import numpy as np
from matplotlib import pyplot as plt
import networkx as nx 
import pandas as pd
from scipy import stats

#En esta seccion se cargan los datos de toda la red

dataset00_w = np.loadtxt("full_set.txt", dtype='int', delimiter=" ", usecols = (6))
dataset00_c = np.loadtxt("full_set.txt", dtype='string', delimiter=" ", usecols = (0,1))

#Aqui le damos el corte, se queda con todos los nodos que tengan valor > 0 en la columna 6 (experimental)

cut0 = np.where(dataset00_w > 0)
cureted_ds0 = []
for i in cut0:
  cureted_ds0.append(dataset00_c[i,:])
cureted_ds0 = np.reshape(cureted_ds0, (np.size(cut0), 2))

G0 = nx.Graph()
G0.add_edges_from(cureted_ds0)

#La matriz de adjacency y el grado de cada nodo

G0_mat = nx.adjacency_matrix(G0)
G0_k = np.sum(G0_mat, axis=0)

#103 porque es el numero de comunidades de infomap

tamanhos = np.zeros((103))
xaxis = np.logspace(0,np.log10(700),11)
x = np.logspace(0,np.log10(700),10)

#Estos vectores se llenan con las cantidades mencionadas para las comunidades que cumplan con el criterio min_size

k_max = [] #El grado maximo
k_mode = [] #La moda de grado
com_id = [] #El id de la comunidad

min_size = 30 #Cantidad minima de nodos en comunidad a evaluar

#Le cargo las comunidades de infomap

for i in range(0,103):
  data = pd.read_table("communities/com_infomap", dtype='str', skiprows = i, delimiter=",", nrows=1)
  a = list(data.values[0]) 
  tamanhos[i] = np.size(a)
  if tamanhos[i] > min_size:
    dum = set(G0.nodes) - (set(G0.nodes) - set(data))   
    l = 0
    arr = np.zeros((len(list(dum))))
    B = list(G0.nodes)
    for j in range(0,np.size(B)):
      for k in range(0,len(dum)):
        if B[j] == list(dum)[k]:
            arr[l] = G0_k[0,j]
            l = l + 1
    k_max.append(np.amax(arr))
    com_id.append(i)
    harr, bi = np.histogram(arr,bins = xaxis)
    k_mode.append(x[np.where(harr == np.amax(harr))])
    col = '%.01d'%(i+1)
    col = '1.'+col
    plt.loglog(x,np.divide(harr,np.sum(harr) + 0.0),color= col)

plt.show()
