#!/usr/bin/env python

# Script para buscar GO terms de ancestros
##############################################################

# nombre historico:
# 1.Script_0_GO_MAP_ANCESTORS_V1
import re

def etapa_1(numero_de_comunidad):

    gBP = open("./1/0.1.Lista_community_" + numero_de_comunidad + "_BP_CON_GEN_ID.txt", 'r')
    rBP = open("./0/R_BP.txt", 'r')

    gMF = open("./1/0.1.Lista_community_" + numero_de_comunidad + "_MF_CON_GEN_ID.txt", 'r')
    rMF = open("./0/R_MF.txt", 'r')

    gCC = open("./1/0.1.Lista_community_" + numero_de_comunidad + "_CC_CON_GEN_ID.txt", 'r')
    rCC = open("./0/R_CC.txt", 'r')

    # creo que estos son los outputs
    foBP = open("./2/0.2.community_" + numero_de_comunidad + "_proteome_crudos_asociados_BP_CON_GEN_ID_ancestors_BP_iiiii.txt", 'w')
    foMF = open("./2/0.2.community_" + numero_de_comunidad + "_proteome_crudos_asociados_MF_CON_GEN_ID_ancestors_MF_iiiii.txt", 'w')
    foCC = open("./2/0.2.community_" + numero_de_comunidad + "_proteome_crudos_asociados_CC_CON_GEN_ID_ancestors_CC_iiiii.txt", 'w')


    BP = []
    MF = []
    CC = []
    dicGObp = {}
    dicGOmf = {}
    dicGOcc = {}

    ## BP
    for row in gBP:
        row = row.split()
        BP.append(row[1])
    #print("GO count BP genomic", len(BP))

    GOcount = 0
    for row in rBP:
        row = row.strip()
        if "$`GO:" in row:
            GOcount += 1
            match = re.search(r'GO:\d{7}', row)
            GO = match.group()
            dicGObp[GO] = []
        else:
            row = row.split("\"")
            for i in row:
                match = re.search(r'GO:\d{7}', i)
                if match:
                    GOances = match.group()
                    dicGObp[GO].append(GOances)
                    
    for i in BP: ##BP es una lista de GO ids que viene del genoma de Xcc
        if i not in dicGObp.keys():
            #print ("BP", i)
            pass
        else:
            foBP.write(i+"\t")  #si esta en el diccionario universal de BPs lo escribe en un archivo "ancestors_BP.txt"
            count = 0
            for x in dicGObp[i]:
                count += 1
                y = 1
                foBP.write(x)
                if count < len(dicGObp[i]):
                    end = " "
                else:
                    end = "\n"
                foBP.write(end)
    #print("GO count BP total", GOcount, len(dicGObp))

    ## MF
    for row in gMF:
        row = row.split()
        MF.append(row[1])
    #print("GO count MF genomic", len(MF))

    GOcount = 0
    for row in rMF:
        row = row.strip()
        if "$`GO:" in row:
            GOcount += 1
            match = re.search(r'GO:\d{7}', row)
            GO = match.group()
            dicGOmf[GO] = []
        else:
            row = row.split("\"")
            for i in row:
                match = re.search(r'GO:\d{7}', i)
                if match:
                    GOances = match.group()
                    dicGOmf[GO].append(GOances)
    for i in MF:
        if i not in dicGOmf.keys():
            #print ("MF", i)
            pass
        else:
            foMF.write(i+"\t")
            count = 0
            for x in dicGOmf[i]:
                count += 1
                y = 1
                foMF.write(x)
                if count < len(dicGOmf[i]):
                    end = " "
                else:
                    end = "\n"
                foMF.write(end)
    #print("GO count MF total", GOcount, len(dicGOmf))


    ### CC
    for row in gCC:
        row = row.split()
        CC.append(row[1])
    #print("GO count CC genomic", len(CC))

    GOcount = 0
    for row in rCC:
        row = row.strip()
        if "$`GO:" in row:
            GOcount += 1
            match = re.search(r'GO:\d{7}', row)
            GO = match.group()
            dicGOcc[GO] = []
        else:
            row = row.split("\"")
            for i in row:
                match = re.search(r'GO:\d{7}', i)
                if match:
                    GOances = match.group()
                    dicGOcc[GO].append(GOances)
    for i in CC:
        if i not in dicGOcc.keys():
            #print ("CC", i)
            pass
        else:
            foCC.write(i+"\t")
            count = 0
            for x in dicGOcc[i]:
                count += 1
                y = 1
                foCC.write(x)
                if count < len(dicGOcc[i]):
                    end = " "
                else:
                    end = "\n"
                foCC.write(end)
    #print("GO count CC total", GOcount, len(dicGOcc))
    foBP.close()
    foMF.close()
    foCC.close()
        
