# This program contains functions for logging robot parameters
# to local files.  The files can be accessed by NodeRed or other programs.

import numpy as np # for handling arrays

def writeFiles(current_phis):
    txt = open("/home/debian/basics/PDL.txt", 'w+') # file for phi dot left
    txt2 = open("/home/debian/basics/PDR.txt", 'w+') # file for phi dot right
    phi_dotL = round(current_phis[0],1)
    phi_dotR = round(current_phis[1],1)
    txt.write(str(round(phi_dotL,1)))
    txt2.write(str(round(phi_dotR,1)))
    txt.close()
    txt2.close()
    
def Node_Red2(val):
    txt = open("/home/debian/SCUTTLE/a.txt",'w+') # file for phi dot left
    txt2 = open("/home/debian/SCUTTLE/b.txt",'w+') # file for phi dot left
    a = round(val[0],2)
    b = round(val[1],2)
    txt.write(str(a))
    txt2.write(str(b))
    txt.close()
    txt2.close() 
    
def csv_write(list):
    list = [str(i) for i in list]
    with open('excel_data.csv', 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(list)
    csvFile.close()

def clear_file():
    open('excel_data.csv','w').close()
