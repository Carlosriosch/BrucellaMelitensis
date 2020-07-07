# -*- coding: utf-8 -*-

from __future__ import division
import numpy as np
from scipy import stats
from operator import itemgetter
import glob

# para una comunidad

def etapa_4(numero_de_comunidades, size_comunidad):

    path_input = "./4/"

    #input_files = ["./4/community_" + numero_de_comunidades + "_comparacion_frecuencias_BP.txt", "./4/community_" + numero_de_comunidades + "_comparacion_frecuencias_CC.txt", "./4/community_" + numero_de_comunidades + "_comparacion_frecuencias_MF.txt"]
    
    input_files = glob.glob(path_input + "community_" + numero_de_comunidades + "_comparacion_frecuencias*.txt")

    #categorias = ["BP", "CC", "MF"]

    output_file = "./4/community_" + numero_de_comunidades + "_enriquecidos_"

    for r in range(len(input_files)):

    #########################

        input = input_files[r]
        
        str1 = input_files[r].split('.')[-2]
        categoria = str1.split('_')[-1]

        # voy a armar la "planilla de excel" en una lista de tuplas. O listas.
        go_terms = np.loadtxt(input, dtype='str', delimiter = '\t', usecols=(0, 1))
        columnas = np.loadtxt(input, dtype='int', delimiter = '\t', usecols=(2, 3, 4, 5))

        planilla = []

        for i in range(len(go_terms)):
            sublista = [go_terms[i][0], go_terms[i][1], columnas[i][0], columnas[i][1], columnas[i][2], columnas[i][3]]
            planilla.append(sublista)
            
        # calculo la distribucion hipergeometrica. Va a ir a parar a una nueva columna, ie, un nuevo casillero de la tupla.
        # h es el p-value de la distribucion
        for i in range(len(planilla)):
            h = stats.hypergeom.pmf(planilla[i][2], planilla[i][5], planilla[i][4], planilla[i][3])
            planilla[i].append(h)
        
        # ahora ordeno las filas (elementos de la lista mas grande) por tamaño del p-value, de manera descendente. Esta en el lugar 6.
        planilla_ordenada = sorted(planilla, key=itemgetter(6))

        # ahora aplico la correccion de Benjamini-Hochson:
        # el cociente para cada p-value es: la cantidad de go terms en la comunidad, sobre el numero de orden del p-value.
        for i in range(len(planilla_ordenada)):
            cociente = len(planilla_ordenada)/(i + 1)
            planilla_ordenada[i][-1] = planilla_ordenada[i][-1]*cociente

        # ahora fijo un corte en 0.05 y veo que terminos estan enriquecidos en esta comunidad
        corte = 0.05
        
        # armo un txt con los terminos enriquecidos

        results = open(output_file + categoria + ".txt", "w")
        
        # agrego informacion adicional en el header:
        # tamaño de la comunidad y cant total de GO terms
        results.write("Tamaño de la comunidad: %d\n" % (size_comunidad))
        # elijo la fila 0 como cualquiera, porque todas tienen el mismo valor en la columna
        cant_total_go_terms_comunidad = planilla_ordenada[0][3]
        results.write("Cantidad total de GO terms en la comunidad: %d\n\n" % (cant_total_go_terms_comunidad))
        
        results.write("codigo\t\tp-value\tenr com\tenr tot\tfrac\tsignificado\n")

        # me hago una planilla nueva, de resultados
        resultados = []
        
        for p in planilla_ordenada:
            if p[-1] <= corte:
            
                # calculo los dos numeros adicionales que nos interesan
                num1 = p[2]/p[3]
                num2 = (p[2]/p[3])/(p[4]/p[5])
                
                # calculo la fraccion que representa el GO term en la comunidad
                frac = num1*cant_total_go_terms_comunidad/size_comunidad
                
                resultados.append([p[0], p[-1], num1, num2, frac, p[1]])
                
                #results.write("%s\t%.2g\t%.4f\t%5.1f\t%.3f\t%s\n" % (p[0], p[-1], num1, num2, frac, p[1]))

        # ordeno por fraccion
        resultados = sorted(resultados, key=itemgetter(4), reverse=True)
        
        for res in resultados:
            results.write("%s\t%.2g\t%.4f\t%5.1f\t%.3f\t%s\n" % (res[0], res[1], res[2], res[3], res[4], res[5]))
        
        results.close()

