# SCRIPTS SUBFOLDER README:

These are linux scripts to run on your beaglebone blue after installing the proper debian image.

## Beaglebone Image:
Please navigate to the "releases" tab of this github to download the latest image.

How to run self_installer.sh:
1) Use the wget command and paste the raw hyperlink of the self_installer.sh into your CLI.
2) use "sudo bash self_installer.sh" to run it
3) The install may take about 5 minutes. At finish, you'll see these characters again: "➜  ~"

How to verify successful installations:
1) Run this command: sudo dpkg-query -f '${binary:Package}\n' -W | wc -l
2) package count after flashing new image: 
2) package count after running self-installer: 475
