# This program contains functions for logging robot parameters
# to local files.  The files can be accessed by NodeRed or other programs.
# Nodered can be found on the beagle at port 1880. ie, 192.168.8.1:1880

import numpy as np # for handling arrays

# A function for populating 2 text files with updated phi-dots
def writeFiles(current_phis): 
    txt = open("/home/debian/basics/PDL.txt", 'w+') # file for phi dot left
    txt2 = open("/home/debian/basics/PDR.txt", 'w+') # file for phi dot right
    phi_dotL = round(current_phis[0],1)
    phi_dotR = round(current_phis[1],1)
    txt.write(str(round(phi_dotL,1)))
    txt2.write(str(round(phi_dotR,1)))
    txt.close()
    txt2.close()

# A function for populating 2 text files with updating variables    
def Node_Red2(val): # this function takes a 2-element array called val
    txt = open("/home/debian/basics/a.txt",'w+') # file for generic variable a
    txt2 = open("/home/debian/basics/b.txt",'w+') # file for generic variable b
    a = round(val[0],2)
    b = round(val[1],2)
    txt.write(str(a))
    txt2.write(str(b))
    txt.close()
    txt2.close() 

# A function for creating a CSV file from a list of values.    
def csv_write(list):
    list = [str(i) for i in list]
    with open('PID_Lab_Data.csv', 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(list)
    csvFile.close()

# A function to clear an existing CSV file
def clear_file():
    open('PID_Lab_Data.csv','w').close()
