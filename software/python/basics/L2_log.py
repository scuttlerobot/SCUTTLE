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
