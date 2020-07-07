#!/usr/bin/env python

# Script para comparar archivos y extraer gene ID y GO terms EN SUBSETS 
#######################################################################

# nombre historico:
# 0.Script_para_comparar_extraer_geneID_y_GO_terms_asociados_de_Uniprot_Bsuis1330.py

import re

def etapa_0(file_comunidad, numero_de_comunidad):

    # File locations and variables
    ##############################

    # Subset a analizar
    # agarro una comunidad
    subset = open(file_comunidad, 'r').readlines()
    lenSubset = len(subset)
    #print("size comunidad: %d" % (lenSubset))

    # Genoma de Bsuis 1330 uniprot con GO terms
    # aca elijo una clasificacion (BP, CC, o MF)
    files_go = ['./0/uniprot-Brucella+melitensis+16M_BP.tab', './0/uniprot-Brucella+melitensis+16M_CC.tab', './0/uniprot-Brucella+melitensis+16M_MF.tab']

    files_output = ["./1/0.1.Lista_community_" + numero_de_comunidad + "_BP_CON_GEN_ID.txt", "./1/0.1.Lista_community_" + numero_de_comunidad + "_CC_CON_GEN_ID.txt", "./1/0.1.Lista_community_" + numero_de_comunidad + "_MF_CON_GEN_ID.txt"]

    ##############################################################

    for r in range(len(files_go)):

        uniprot = open(files_go[r], 'r').readlines()
        lenGOterms = len(uniprot)

        # aca el tipo escribe la proteina con todos los go terms que tiene asociados en esa clasificacion.
        # una proteina puede estar en mas de una lista
        outputFile = open(files_output[r], "w")
        #print(files_output[r])

        # Abrir lista de 
        for i in range(1,lenSubset):
            #print(subset)
            lineSubset = subset[i].split()
            #print(lineSubset)
            lineSubset = lineSubset[0]
            

            
            # Abrir lista uniprot
            for j in range(1,lenGOterms):
                lineGO= uniprot[j].split()
                lineGO=' '.join(lineGO)
                
                if lineSubset in lineGO:
                    #print(lineGO)
                    GOs = (re.findall('GO:[\d]+', lineGO))
                    #print(GOs)
                    length=len(GOs)
                    #print(length)
                    #print(length == 0)
                    #print(length != 0)
                    #print('#\n###\n\n')
                    
                    BAW = re.findall('BAWG_[\d]{4}',lineGO)
                    #print('BAW', BAW)


                    if BAW != []:
                        node = str(BAW[0])



                    if length != 0:
                        for k in range(0,(length)):
                            #print 'GOs',GOs
                            #print 'length', length
                            #print('k', k)
                            #print(GOs[k])
                            #print('\n\n\n')
                            outputFile.write('\t' + node + '\t' + GOs[k] + '\n')
                            

        outputFile.close()
    return(lenSubset)
