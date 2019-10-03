
from mfrc522 import SimpleMFRC522
reader = SimpleMFRC522()

def read_rfid():
    id, text = reader.read()    # Read RFID Serial Number and Data
    return (id, text)           # Reurn Serial Number and Data

def write_rfid(text):
    reader.write(text)          # Write data to RFID
