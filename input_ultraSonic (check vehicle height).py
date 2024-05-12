# Contains function to read data from ultrasonic sensor
# Created By : Team A12: Nudara, Cooper, Devni, Kristian, Naailah
# Created Date: 20/04/2024
# version: 5.0

from pymata4 import pymata4
import time

def ultraSonic(triggerPin,echoPin,board,ultrasonicData, sensorHeight):
    '''
    Function to read data from ultrasonic sensor
        Parameters:
            triggerPin (int): pin on the arduino connected to the sensor's trigger
            echoPin (int): pin on the arduino connected to the sensor's echo
            board: communication set-up with arduino
            ultrasonicData (list of integers): list of latest values (distances in cm) polled from the sensor
            sensorHeight (float): height of the ultrasonic sensor from the sruface (cm)
        Returns:
            Function returns updated ultraSonicData
    '''

    board.set_pin_mode_sonar(triggerPin, echoPin, timeout=20000)
    vals = board.sonar_read(triggerPin)

   
    adjustedDistance = sensorHeight - vals[0]

    if adjustedDistance >= 0:
        ultrasonicData.append(adjustedDistance)

        if len(ultrasonicData)==2:    
            ultrasonicData.pop(0)

        print(f'\nHeight of vehicle: {ultrasonicData}')

    else:
        print("\n == NEGATIVE VEHICLE HEIGHT DETECED. CHECK ULTRASONIC SENSOR HEIGHT ==")
        time.sleep(1)

    time.sleep(0.5)


    return ultrasonicData

def main():
    board = pymata4.Pymata4()
    sensorHeight2 = 28
    ultrasonicData2 = []
    triggerPin2 = 7
    echoPin2 = 8

    while True:
        ultraSonic(triggerPin=triggerPin2, echoPin=echoPin2, board=board, ultrasonicData=ultrasonicData2, sensorHeight=sensorHeight2)

if __name__ == '__main__':
    main()
