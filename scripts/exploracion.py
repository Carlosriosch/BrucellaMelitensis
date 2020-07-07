from __future__ import division
import networkx as nx
import matplotlib.pylab as plt
import numpy as np
"""
def ldata(archive):
    f=open(archive)
    data=[]
    for line in f:
        line=line.strip()
        col=line.split()
        data.append(col)
    return data
"""
archivos = ["../dataset/4000.txt", "../dataset/6000.txt", "../dataset/8000.txt", "../dataset/10000.txt", "../dataset/11000.txt"]
titulos = ["Top 4000", "Top 6000", "Top 8000", "Top 10000", "Top 11000"]

for i in range(len(archivos)):

    lista = np.loadtxt(archivos[i], dtype='str', delimiter=" ", usecols = (0, 1))

    G = nx.Graph()
    G.add_edges_from(lista)
    nx.draw(G, font_weight='bold', node_size=20)
    plt.suptitle(titulos[i])
    plt.savefig("../plots/" + titulos[i] + ".png")
    #plt.show()

