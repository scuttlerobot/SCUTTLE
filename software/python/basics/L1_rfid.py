# This module allows the ability to read/write to RFID's.
# Before running the code, you need to install a modified version
# of the MFRC522-python library using the commands below.
# git clone https://github.com/ansarid/MFRC522-python
# cd MFRC522-python
# sudo python3 setup.py install

from mfrc522 import SimpleMFRC522
reader = SimpleMFRC522()

def read_rfid():
    id, text = reader.read()    # Read RFID Serial Number and Data
    return (id, text)           # Return Serial Number and Data

def write_rfid(text):
    reader.write(text)          # Write data to RFID

#=======================================================================================================================#

# UNCOMMENT THE SECTION BELOW TO RUN AS STANDALONE CODE
# Read RFID

# while 1:
#     sn, data = read_rfid()  # Read card serial number and data and store to sn and data variables
#     print("Serial Number: ", sn, "\t Data: ", data) # Print serial number and data

#=======================================================================================================================#

# # UNCOMMENT THE SECTION BELOW TO RUN AS STANDALONE CODE
# # Write To RFID

# print("Place RFID on RFID writer.")
# write_rfid("Hello World!")  # Write "Hello World!" to RFID
# print("Written")
