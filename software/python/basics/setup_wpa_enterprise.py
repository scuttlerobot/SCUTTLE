# run this file to connect to a WPA2 Enterprise wifi network.
# after running once, the beaglebone automatically connects
# unless a network change was made. In order to connect to a
# different WPA2-Enterprise network, update the SSID by changing
# the "search" string.
# last edited 2019.04

# Import necessary libraries

import subprocess   # Runs commands and gets output
import socket		# Used to test internet connection
import os		    # Used to run system commands and checks if run as root user
import getpass 		# Used to hide user input in password field

# Check if the user that executed this program is root

user = os.getenv("SUDO_USER")
if user is None:						                        # If not root
    print("\n   Execute as \033[1;31;48msudo\033[1;37;48m\n")   # Prints request to run as root
    exit()							                            # Closes program


def internet(host="8.8.8.8", port=53, timeout=3):		        # Function to check if internet connection is successful
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception as ex:
        print(ex)
        return False


#       Enter wifi name here.
search = "tamulink-wpa"						                                    # SSID to seach for tamulink-wpa.
ssid = search					      		                                    # Also accepts parts of SSID like, "tam" or "link"

scan = subprocess.Popen(["connmanctl", "services"], stdout=subprocess.PIPE)	    # Run connmanctl services and get output
ssids = scan.stdout.readlines()							                        # Break output into list named "ssids"

print("\n\033[1;32;40mSearching For SSID:\033[1;37;40m", ssid)	                # Print SSID that is being searched for

os.system("echo \"nameserver 8.8.8.8\" >> /etc/resolv.conf")	                # Writes "nameserver 8.8.8.8" to /etc/resolv.conf

while len(ssids) <= 1:					                                        # Checks how many SSIDs where found during scan
    print("Scanning for more SSIDS")		                                    # Scans again if no SSIDs were found
    subprocess.call("connmanctl", " scan", " wifi")	                            # Runs system command to scan for more ssids
    print("Have ", len(ssids), " ssids.")		                                # Prints number of SSIDs found after scan

for x in range(len(ssids)):		                                                # Looks at each SSID in list and converts each list entry to string
    ssids[x] = str(ssids[x])		                                            # Convert to string

for idx, val in enumerate(ssids):	                                            # Search through list for specified SSID or specified part of SSID
    if ssid in val:			                                                    # If found SSID
        ssid = val		                                                        # Replace specified SSID with found SSID

ssid = ssid[0:len(ssid)-3].split()	                                            # Split SSID string along space chars and store in list
del ssid[0]				                                                        # Delete first entry in list because it's an artifact from
                                                                                # bytes to sting in lines 44 and 45

print("\033[1;32;40m\nFound: \n\033[1;37;40m" + ssid[0] + "\t\t" + ssid[1])	    # Output SSID found matching search string

username = input("\n\033[1;37;40mPlease enter your username: \033[0;37;40m")    # Ask for tamulink-wpa username
password = getpass.getpass(prompt='\033[1;37;40mPlease enter your password: \033[0;37;40m', stream=None)    # Ask for tamulink-wpa password

config_path = "/var/lib/connman/" + ssid[1] + ".config"		                                                # Generate connmanctl wifi configuration file path and name

file = open(config_path, "w")	                                                                            # Open file using generated name and path, will create if file is non-existant

print("\033[1;32;40m\nGenerated Configuration File Path: \n\033[1;37;40m" + config_path + "\n")		        # Tell user configuration file name and path

connmanctl_ssid = ssid[1].splits("_")		                                                                # Split connmanctl wifi scan wireless details

file.write("[service_" + ssid[1] + "]\n")		                                                            # Use tamulink detailed ssid for file title
file.write("Type = wifi\n")				                                                                    # this is a WiFi file
file.write("SSID = " + connmanctl_ssid[2] + "\n")	                                                        # Set SSID to detailed SSID
file.write("EAP = peap\n")				                                                                    # Set type of encapsulation
file.write("Phase2 = MSCHAPV2\n")			                                                                # Set type of authentication for network
file.write("Identity= " + username + "\n")		                                                            # Set network username
file.write("Passphrase= " + password + "\n")		                                                        # Set network password

file.close()						                                                                        # Close file

os.system("sudo systemctl restart connman")		                                                            # Restart connman service so it finds new configuration file
