# nombre historico:
# conteo_go.py

from __future__ import division
from collections import Counter
import numpy as np
import glob
import os

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1
    
def ldata(archive):
    f=open(archive)
    data=[]
    for line in f:
        line=line.strip()
        col=line.split()
        data.append(col)
    return data
    
path_input = "./2/"
path_output = "./3/"

def etapa_2(numero_de_comunidad):

    #print(numero_de_comunidad)

    files = glob.glob(path_input + "*community_" + numero_de_comunidad + "_*.txt")

    # ojo con lo siguiente: hay algunas comunidades para las que no se encuentra ningun GO term para ciertas categorias. Eso hace que algunos de los input files de arriba esten vacios. El codigo que sigue no lo sabe manejar, entonces antes de ejecutarlo hago una limpieza, eliminando input files vacios. Al final del dia va a haber algunos "./4/community_*_enriquecidos_*.txt" que no van a estar.

    files_curado = []
    for f in files:
        # si el file no esta vacio...
        if os.stat(f).st_size != 0:
            # ...me lo quedo
            files_curado.append(f)
    
    #print(files)
    
    for f in files_curado:
        #print(f)
        # esta etiqueta la voy a usar para darle nombre a los txt de output.
        # notar que tire el 0.2 que tenia. De todos modos habria que simplificar la nomenclatura
        etiqueta = f.split('.', -1)[-2]
        
        # cargo un file y cuento cuantos hay de cada cosa
        data = np.loadtxt(f, dtype = 'str', delimiter = '\n')

        # data es una lista que tiene en cada casillero varios GO. Agarro cada casillero y hago un split de todos los terminos. Luego junto todo en una sola lista.
        lista = []
        sublista = []

        # esto no funciona para una sola linea
        # lo arregle usando ldata en el caso de una sola linea
        if file_len(f) > 1:
            for d in data:
                sublista.append(d.split())
                #print(d.split())
        else:
            sublista.append(ldata(f)[0])

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
        results = open(path_output + "0.3." + etiqueta + "_proporciones.txt", "w")

        #results.write("GO term\t\tocurrencias\n")
        for p in proporciones:
            results.write("%s\t%d\n" % (p[0], p[1]))
        results.close()
