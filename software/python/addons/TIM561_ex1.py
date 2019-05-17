#Barebones program to grab data from the lidar unit.
#library is located at http://www.github.com/ansarid/pysicktim

# Import pysicktim Library as "lidar"
import pysicktim as lidar

# Repeat code nested in for loop 10 times
for x in range(10):
# while True:

	lidar.scan()	# Requests and returns list of LIDAR
					# distance information in meters

	print(lidar.scan.distances)		# print distance list for latest scan
