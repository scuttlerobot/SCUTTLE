# run this file to connect to the WPA2 Enterprise wifi network

import subprocess
import socket
import os
import time

user = os.getenv("SUDO_USER")
if user is None:
    print("\n   Execute as \033[1;31;48msudo\033[1;37;48m\n")
    exit()

def internet(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception as ex:
        print(ex)
        return False

search = "tamulink-wpa"
ssid = search

scan = subprocess.Popen( ["connmanctl","services"], stdout=subprocess.PIPE)
ssids = scan.stdout.readlines()

print("\n\033[1;32;40mSearching For SSID:\033[1;37;40m", ssid)

os.system("echo \"nameserver 8.8.8.8\" >> /etc/resolv.conf")

#try:

while len(ssids) <= 1:
	print("Scanning for more SSIDS")
	subprocess.call("connmanctl"," scan"," wifi")
	print("Have ", len(ssids), " ssids.")

for x in range(len(ssids)):
  ssids[x] = str(ssids[x])

for idx, val in enumerate(ssids):
	if ssid in val:
		ssid = val

ssid = ssid[0:len(ssid)-3].split()
del ssid[0]

print("\033[1;32;40m\nFound: \n\033[1;37;40m" + ssid[0] + "\t\t" + ssid[1])

username = input("\n\033[1;37;40mPlease enter your username: \033[0;37;40m")
password = input("\033[1;37;40mPlease enter your password: \033[0;37;40m")

config_path = "/var/lib/connman/" + ssid[1] + ".config"

file = open(config_path,"w")

print("\033[1;32;40m\nGenerated Configuration File Path: \n\033[1;37;40m" + config_path + "\n")

connmanctl_ssid = ssid[1].split("_")

file.write("[service_"+ ssid[1] + "]\n")
file.write("Type = wifi\n")
file.write("SSID = " + connmanctl_ssid[2] + "\n")
file.write("EAP = peap\n")
file.write("Phase2 = MSCHAPV2\n")
file.write("Identity= " + username + "\n")
file.write("Passphrase= " + password + "\n")

file.close()

os.system("sudo systemctl restart connman")

time.sleep(2)

if internet() == True:
    print("\033[1;32;40m\nConnected!\n")
    exit()

else:
    print("\033[1;31;48mNot connected!\n")

#except:
print("\033[1;31;40m" + search, "not found!\n")
exit()
