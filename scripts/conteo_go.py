from __future__ import division
from collections import Counter
import numpy as np
import glob

path_input = "../GO_analysis_PPI_Brucella/2.GO_crudos_y_ancestors/"
path_output = "../GO_analysis_PPI_Brucella/3.GO_proporciones/"

files = glob.glob(path_input + "*CON_GEN_ID_ancestors*.txt")

for f in files:
    
    # esta etiqueta la voy a usar para darle nombre a los txt de output.
    # notar que tire el 0.2 que tenia. De todos modos habria que simplificar la nomenclatura
    etiqueta = f.split('.', -1)[-2]
    
    # cargo un file y cuento cuantos hay de cada cosa
    data = np.loadtxt(f, dtype = 'str', delimiter = '\n')

    # data es una lista que tiene en cada casillero varios GO. Agarro cada casillero y hago un split de todos los terminos. Luego junto todo en una sola lista.
    lista = []
    sublista = []

    for d in data:
        sublista.append(d.split())

    for s in sublista:
        for ss in s:
            lista.append(ss)

    # ahora cuento las ocurrencias de cada termino. Diccionario que tiene el GO term con la cantidad de ocurrencias
    cuentas = Counter(lista)

    # para dar la proporcion, calculo la cantidad de elementos
    size = len(lista)

    proporciones = {}
    for c in cuentas:
        proporciones[c] = cuentas[c]
        #print(c, cuentas[c])

    # ordeno
    proporciones = sorted(proporciones.items(), key=lambda kv: kv[1])
    proporciones = proporciones[::-1]

    # ahora lo escribo
    results = open(path_output + etiqueta + "_proporciones.txt", "w")

    results.write("GO term\t\tocurrencias\n")
    for p in proporciones:
        results.write("%s\t%d\n" % (p[0], p[1]))
    results.close()
