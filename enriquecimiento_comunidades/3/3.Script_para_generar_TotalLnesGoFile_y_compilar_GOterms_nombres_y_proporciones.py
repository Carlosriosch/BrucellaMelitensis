#!/usr/bin/env python

# Script para generar total_GO_terms_por_categoria.txt file
# y para compilar GO terms, nombres y proporciones
#######################################################################

# Modulos #####
import re
import os
###############


# Generar total_GO_terms_por_categ file   #
###########################################
# File locations and variables I ####     #
outputfile0 = open('total_lines_GO_por_categoria.txt', 'w')
############################              #
                                          #

for filename in sorted(os.listdir('../2.GO_crudos_y_ancestors/')):
    if '0.2.' in filename and '.txt' in filename:
        arch = open('../2.GO_crudos_y_ancestors/%s' %(filename), 'r').read()
        lista = re.findall('GO:', arch)

		# Escribir total GO terms file
        outputfile0.write(str(len(lista)) + '\t' + filename + '\n')
										  #
outputfile0.close()                       #
###########################################




# File locations and variables II #################
###################################################

# GO proportions del subset a analizar
subsetFile=raw_input('Subset file?: ')
subset=open(subsetFile, 'r').readlines()
lenSubset=len(open(subsetFile, 'r').readlines())
prefix=subsetFile[10:14]
sufix=subsetFile[-6:-4]

# GO proportions en el genoma para la misma categoria (CC, MF, o BP)
GenomProporFile=raw_input('File Genome proportions?: ')
GenomPropor=open(GenomProporFile, 'r').readlines()
lenGenomPropor=len(open(GenomProporFile, 'r').readlines())


# Dicccionario de ALL GO terms y nombres
dicc=open('DICTIONARY_ALL_GO_terms.txt','r').readlines()
lendicc=len(open('DICTIONARY_ALL_GO_terms.txt','r').readlines())

# Numero total de GO terms en cada categoria
totalFile =open('total_lines_GO_por_categoria.txt','r').readlines()
lenTotalFile=len(open('total_lines_GO_por_categoria.txt','r').readlines())

outputFile = open("../4.GO_comparacion_frecuencias/%s_comparacion_frecuencias_%s.txt" %(prefix,sufix), "w")
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
								print lineGenomPropor
								print GOid in lineGenomPropor[0]
								print '\n'	
								if GOid in lineGenomPropor[0]: 
									frecGenom = lineGenomPropor[1] 

									# Escribir outputFile
									outputFile.write(GOid + '\t' + name + '\t' + prop + '\t' + subsetdivisor + '\t' + frecGenom + '\t' + genomedivisor + '\n')
									break


outputFile.close()
	
