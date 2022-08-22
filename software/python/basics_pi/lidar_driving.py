#!/usr/bin/python3
# Drive the SCUTTLE while visualizing a simple LIDAR point cloud in NodeRED

import socket
import json
import numpy as np
import L1_lidar as lidar
import L2_vector as vec
import L2_speed_control as sc
from time import sleep
from threading import Thread

class SCUTTLE:

    def __init__(self):

        #Kinematics#
        self.wheelRadius = 0.04
        self.wheelBase = 0.1
        self.A_matrix = np.array([[1/self.wheelRadius, -self.wheelBase/self.wheelRadius], [1/self.wheelRadius, self.wheelBase/self.wheelRadius]])
        self.max_xd = 0.4
        self.max_td = (self.max_xd/self.wheelBase)

        #UPD communication#
        self.IP = "127.0.0.1"
        self.port = 3553
        self.dashBoardDatasock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.dashBoardDatasock.bind((self.IP, self.port))
        self.dashBoardDatasock.settimeout(.25)

        #NodeRED data in#
        self.dashBoardData = None

        #LIDAR Thread#   
        lidarThread = Thread(target=self.scan_loop, daemon=True)
        lidarThread.start()

        #NodeRED Data Thread#
        self.dashBoardDataThread = Thread(target=self._dashBoardDataLoop, daemon=True)
        self.dashBoardDataThread.start()

        #Driving Thread#
        self.controlThread = Thread(target=self._controlLoop, daemon=True)
        self.controlThread.start()

    def scan_loop(self):
        while True:
            data = self.cartesian_scan()
            data_msg = data.encode('utf-8')
            self.dashBoardDatasock.sendto(data_msg, ("127.0.0.1", 3555))
            sleep(.025)

    def cartesian_scan(self):
        rows = ''
        polar_data = lidar.polarScan(num_points=100)

        for d,t in polar_data:
            cartesian_point = vec.polar2cart(d,t)
            rows += self.format_row(cartesian_point)

        return rows[:-1]

    # Format the x,y lidar coordinates so that the bubble-chart can display them
    def format_row(self, point, r=3):
        x, y = point
        return '{x: ' + str(x) + ', y: ' + str(y) + ', r:' + str(r) + '},'

    def _dashBoardDataLoop(self):
        while True:
            try:
                dashBoardData,recvAddr = self.dashBoardDatasock.recvfrom(1024)
                self.dashBoardData = json.loads(dashBoardData)

            except socket.timeout:
                self.dashBoardData = None

    def _controlLoop(self):
        while True:
            if self.dashBoardData != None:
                try:
                    userInputTarget = self.dashBoardData['one_joystick']
                    wheelSpeedTarget = self._getWheelSpeed(userInputTarget)
                    sc.driveOpenLoop(wheelSpeedTarget)
                except: 
                    pass

    def _getWheelSpeed(self,userInputTarget):
        try:
            robotTarget = self._mapSpeeds(np.array([userInputTarget['y'],-1*userInputTarget['x']]))
            wheelSpeedTarget = self._calculateWheelSpeed(robotTarget)
            return wheelSpeedTarget
        except:
            pass
    
    def _mapSpeeds(self,original_B_matrix):
        B_matrix = np.zeros(2)
        B_matrix[0] = self.max_xd * original_B_matrix[0]
        B_matrix[1] = self.max_td * original_B_matrix[1]
        return B_matrix

    def _calculateWheelSpeed(self,B_matrix):
        C_matrix = np.matmul(self.A_matrix,B_matrix)
        C_matrix = np.round(C_matrix,decimals=3)
        return C_matrix


    def getdashBoardData(self):
        return self.dashBoardData


if __name__ == "__main__":

    robot = SCUTTLE()
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        print("Stopping robot")