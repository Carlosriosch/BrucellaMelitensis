from shutil import copyfile
import glob

def sep():

    files = glob.glob("./4/*enriquecidos*.txt")

    for f in files:
        str = f.split('\\')[1]
        
        dst = "./resultados/" + str
        copyfile(f, dst)