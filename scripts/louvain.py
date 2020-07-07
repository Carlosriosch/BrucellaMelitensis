from __future__ import division
import networkx as nx
from community import community_louvain
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.cm import get_cmap

lista = np.loadtxt("../dataset/11000.txt", dtype='str', delimiter=" ", usecols = (0, 1))

G = nx.Graph()
G.add_edges_from(lista)

nodos_lcc = max(nx.connected_components(G), key=len)

LCC = G.subgraph(nodos_lcc)

# esto es un dict
particion = community_louvain.best_partition(LCC)

cant_grupos = max(particion[p] for p in particion) + 1

particion_ordenada = sorted(particion.items(), key=lambda kv: kv[1])

grupos = []

for i in range(cant_grupos):
    grupos.append([])

for u,v in particion_ordenada:
        for i in range(cant_grupos):
            if int(v) == i:
                grupos[i].append(u)

# imprimir comunidad_id, tamaño, grado maximo, id del grado maximo
results = open("../datos_comunidades_lcc.txt", "w")
results.write("COMM\tSIZE\tGR. MAX.\tID GR. MAX.\n")
for i in range(cant_grupos):
    #print("Grupo", i)
    grado_max = max(LCC.degree(n) for n in grupos[i])
    
    id_grado_max = []
    
    for n in grupos[i]:
        if LCC.degree(n) == grado_max:
            id_grado_max.append(n)
            #print(n)
    
    results.write("%d\t\t%d\t\t%d\t\t" % (i, len(grupos[i]), grado_max))
    
    # si hay mas de una proteina con grado maximo, quiero que me imprima todos los id uno al lado del otro, y despues haga un newline
    for g in id_grado_max:
        results.write("\t%s" % (g))
    results.write("\n")
results.close()



"""
results = open("../particion_louvain_lcc.txt", "w")
results.write("NODO\t\tCOMM\tGRADO\n")
for p in particion_ordenada:
    results.write("%s\t%d\t%d\n" % (p[0], p[1], LCC.degree(p[0])))
results.close()
"""


"""
colores_id = np.linspace(0, 1, cant_grupos)
cmap = get_cmap('jet')

color_map = []

for node in LCC:
    for i in range(cant_grupos):
        if particion[str(node)] == i:
            color_map.append(colores_id[i])

nx.draw(LCC, node_color = color_map, node_size=40)
plt.suptitle("Comp. Gigante - Louvain", fontsize = 18)
#plt.savefig("../comunidades_lcc.png")

plt.show()
"""

