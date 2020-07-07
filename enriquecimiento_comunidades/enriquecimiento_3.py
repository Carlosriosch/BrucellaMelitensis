#!/usr/bin/env python

# Script para generar total_GO_terms_por_categoria.txt file
# y para compilar GO terms, nombres y proporciones

# nombre historico:
# 3.Script_para_generar_TotalLnesGoFile_y_compilar_GOterms_nombres_y_proporciones

#######################################################################

# Modulos #####
import re
import os
import glob
###############

def etapa_3(numero_de_comunidad):
    
    path_input = "./3/"
    
    # estos inputs son los que se calcularon en la etapa 2, ex web
    #input_files_comunidad = ["./3/0.3.community_" + numero_de_comunidad + "_proteome_crudos_asociados_BP_CON_GEN_ID_ancestors_BP_iiiii_proporciones.txt", "./3/0.3.community_" + numero_de_comunidad + "_proteome_crudos_asociados_CC_CON_GEN_ID_ancestors_CC_iiiii_proporciones.txt", "./3/0.3.community_" + numero_de_comunidad + "_proteome_crudos_asociados_MF_CON_GEN_ID_ancestors_MF_iiiii_proporciones.txt"]
    
    input_files_comunidad = glob.glob(path_input + "*community_" + numero_de_comunidad + "_*.txt")

    # estos se calcularon igual, pero no hace falta calcularlos cada vez
    #input_files_genoma = ["./3/0.3.Bmelitensis16M_nodes_proportions_BP.txt", "./3/0.3.Bmelitensis16M_nodes_proportions_CC.txt", "./3/0.3.Bmelitensis16M_nodes_proportions_MF.txt"]

    #categorias = ["BP", "CC", "MF"]

    etiqueta_comunidad = str(numero_de_comunidad)

    #########################################################################


    for r in range(len(input_files_comunidad)):
        
        # obtengo la categoria a partir del input file:
        str1 = input_files_comunidad[r].split('.')[-2]
        categoria = str1.split('_')[-3]
        
        #genoma = input_files_genoma[r]
        # agarro solo el genoma de la categoria
        # le pongo el indice 0 porque glob me lo mete en una lista, y espero que siempre sea un solo elemento
        genoma = glob.glob(path_input + "*Bmelitensis*" + categoria + ".txt")[0]

        # Generar total_GO_terms_por_categ file   #
        ###########################################
        # File locations and variables I ####     #
        outputfile0 = open('./3/total_lines_GO_por_categoria.txt', 'w')
        ############################              #
                                                  #

        for filename in sorted(os.listdir('./2/')):
            if '0.2.' in filename and '.txt' in filename:
                arch = open('./2/%s' %(filename), 'r').read()
                lista = re.findall('GO:', arch)

                # Escribir total GO terms file
                outputfile0.write(str(len(lista)) + '\t' + filename + '\n')
                                                  #
        outputfile0.close()                       #
        ###########################################




        # File locations and variables II #################
        ###################################################

        # GO proportions del subset a analizar
        subsetFile = input_files_comunidad[r]
        subset=open(subsetFile, 'r').readlines()
        lenSubset=len(open(subsetFile, 'r').readlines())
        #prefix=subsetFile[10:14]
        #sufix=subsetFile[-6:-4]
        
        #prefix = "community_" + etiqueta_comunidad
        
        # aca arriba se puden confundir todas las que empiezan con el mismo numero. Capaz tendria que agregar un "_"
        prefix = "community_" + etiqueta_comunidad
        
        #sufix = categorias[r]
        sufix = categoria

        # GO proportions en el genoma para la misma categoria (CC, MF, o BP)
        GenomProporFile = genoma
        GenomPropor=open(GenomProporFile, 'r').readlines()
        lenGenomPropor=len(open(GenomProporFile, 'r').readlines())


        # Dicccionario de ALL GO terms y nombres
        dicc=open('./3/DICTIONARY_ALL_GO_terms.txt','r').readlines()
        lendicc=len(open('./3/DICTIONARY_ALL_GO_terms.txt','r').readlines())

        # Numero total de GO terms en cada categoria
        totalFile =open('./3/total_lines_GO_por_categoria.txt','r').readlines()
        lenTotalFile=len(open('./3/total_lines_GO_por_categoria.txt','r').readlines())

        outputFile = open("./4/%s_comparacion_frecuencias_%s.txt" %(prefix,sufix), "w")
        ###################################


        # Abrir GO porportions del subset a analizar y extraer GO term y proporcion
        for m in range(0,lenSubset):
            lineSubset = subset[m].split()
            #print lineSubset[0], lineSubset[1]
            GOid = lineSubset[0]
            prop = lineSubset[1]
                
            # Buscar el nomnbre de la GOid en el diccionario
            for j in range(0,lendicc):
                linedicc = dicc[j].rstrip('\n').split('\t')
                
                if GOid == linedicc[0]:
                    name = linedicc[1]
                    #print name		
                    # Buscar el numero total de GO terms en el total (crudos + ancestros) del subset para la misma categoria
                    for l in range(0,lenTotalFile):
                        linetot = totalFile[l].split()
                        #print linetot
                        #print prefix
                        #print sufix
                        #print linetot[1]
                        #print prefix in linetot[1]  
                        #print sufix in linetot[1]
                        #print '\n'
                        if prefix in linetot[1] and sufix in linetot[1]:
                            subsetdivisor = linetot[0]
                            #print 'subsetdivisor' + subsetdivisor
                            
                            # Buscar el numero total de GO terms en el total (crudos + ancestros) del genoma para la misma categoria
                            for l in range(0,lenTotalFile):
                                linetot = totalFile[l].split()
                                
                                if 'Bmel' in linetot[1] and sufix in linetot[1]:
                                            
                                    genomedivisor = linetot[0] #
                                    #print 'genomdivisor' + genomedivisor
                                    # Buscar proporcion del GOid en el genoma para la misma categoria
                                    for m in range(0,lenGenomPropor): 
                                        #print 'm',m
                                        lineGenomPropor = GenomPropor[m].split() 
                                        #print(lineGenomPropor)
                                        #print(GOid in lineGenomPropor[0])
                                        #print('\n')
                                        if GOid in lineGenomPropor[0]: 
                                            frecGenom = lineGenomPropor[1] 

                                            # Escribir outputFile
                                            outputFile.write(GOid + '\t' + name + '\t' + prop + '\t' + subsetdivisor + '\t' + frecGenom + '\t' + genomedivisor + '\n')
                                            break


        outputFile.close()
	
