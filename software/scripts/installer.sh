#!/bin/bash

# Promt for root password
[ "$UID" -eq 0 ] || exec sudo bash "$0" "$@"

# Check for internet connection.
printf "\nChecking for internet connection.\n"
wget -q --spider http://google.com
if [ $? -eq 0 ]; then
    echo -e "\n\e[1m\e[32mConnected.\e[0m\n"
else
    echo -e "\n\e[1m\e[31mERROR: No Internet Connection!\e[0m"
    exit
fi

echo -e "\nUpdating & Upgrading.\n"

apt update >/dev/null 2>&1
apt upgrade -y >/dev/null 2>&1
apt dist-upgrade -y >/dev/null 2>&1
apt --fix-broken install -y >/dev/null 2>&1
apt autoremove -y >/dev/null 2>&1

echo -e "\nInstalling APT Packages.\n"

apt_packages=$(cat ./packages/apt_packages.txt | tr "\n" " ")
IFS=' ' read -r -a apt_packages <<< "$apt_packages"
arr_len=${#apt_packages[@]}
for (( i=1; i<${arr_len}+1; i++ ));
do
    echo -n "APT:[$i/${#apt_packages[@]}] Installing ${apt_packages[$i-1]}."
    log=$(apt install -qq -y "${apt_packages[$i-1]}" >/dev/null 2>&1)
    if [ $? != 0 ]; then
        echo $log
    fi
    echo -e "\r\e[1m\e[32mAPT:[$i/${#apt_packages[@]}] Installed ${apt_packages[$i-1]}. ✓\e[0m"
done

echo -e "\nInstalling Pip3 Packages.\n"

pip3_packages=$(cat ./packages/pip3_packages.txt | tr "\n" " ")
IFS=' ' read -r -a pip3_packages <<< "$pip3_packages"
arr_len=${#pip3_packages[@]}
for (( i=1; i<${arr_len}+1; i++ ));
do
    echo -n "PIP3:[$i/${#pip3_packages[@]}] Installing ${pip3_packages[$i-1]}."
    log=$(pip3 install "${pip3_packages[$i-1]}" >/dev/null 2>&1)
    if [ $? != 0 ]; then
        echo $log
    fi
    echo -e "\r\e[1m\e[32mSnap:[$i/${#pip3_packages[@]}] Installed ${pip3_packages[$i-1]}. ✓\e[0m"
done

apt update >/dev/null 2>&1
apt upgrade -y >/dev/null 2>&1
apt dist-upgrade -y >/dev/null 2>&1
apt --fix-broken install -y >/dev/null 2>&1
apt autoremove -y >/dev/null 2>&1
apt autoclean -y >/dev/null 2>&1

# final_file=./final.sh
# if test -f "$final_file"; then
#     bash ./final.sh
# fi

