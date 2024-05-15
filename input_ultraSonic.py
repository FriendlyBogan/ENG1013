# Contains function to read data from ultrasonic sensor
# Created By : Team A12: Nudara, Cooper, Devni, Kristian, Naailah
# Created Date: 20/04/2024
# version: 5.0

from pymata4 import pymata4
import time

velList = []

def ultrasonic_sensor(triggerPin,echoPin,board,ultrasonicData, distanceTimer):

    '''
    Function to read data from ultrasonic sensor
        Parameters:
            triggerPin (int): pin on the arduino connected to the sensor's trigger
            echoPin (int): pin on the arduino connected to the sensor's echo
            board: communication set-up with arduino
            ultrasonicData (list of integers): list of latest values (distances in cm) polled from the sensor
            distanceTimer (int): counter for counting how many seconds distance is detected for
        Returns:
            Function returns updated ultraSonicData
    '''

    board.set_pin_mode_sonar(triggerPin, echoPin, timeout=20000)
    vals = board.sonar_read(triggerPin)

    ultrasonicData.append((vals[0])) #only appending the distance

    if len(ultrasonicData) > 2:
        vel = round((ultrasonicData[-2]-ultrasonicData[-1])/(3),2)
        print(f'velocity = {vel}cm/sec')
        if vel > 10:
            print('Vehicle speed is over 10cm/s!, Alarms sound')

    if stage == 'StageOne':
        if len(ultrasonicData) > 2:
            velList.append(vel)
            if len(velList) >= 2:
                if velList[-1] == velList [-2]:
                    distanceTimer += 1
                    if distanceTimer > 3:
                        print('\n == CONSTANT DISTANCE DETECTED ==')
                else:
                    distanceTimer = 0
    
    if len(ultrasonicData)==8:    
        ultrasonicData.pop(0)

    if len(velList)==8:
        velList.pop(0)

    print(f'\nData from sensor: {ultrasonicData}')

    time.sleep(0.5)

    return ultrasonicData, distanceTimer
  
def main():
    distanceTimer = 0
    board = pymata4.Pymata4()
    ultrasonicData = []
    while True:
        ultrasonicData, distanceTimer = ultrasonic_sensor(triggerPin=5, echoPin=6, board=board, ultrasonicData=ultrasonicData, distanceTimer=distanceTimer)

if __name__ == '__main__':
    main()