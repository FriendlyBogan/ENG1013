# Contains function to read data from ultrasonic sensor
# Created By : Team A12: Nudara, Cooper, Devni, Kristian, Naailah
# Created Date: 20/04/2024
# version: 5.0

from pymata4 import pymata4
import time

def ultra_sonic(triggerPin,echoPin,board,ultrasonicData, predeterminedHeight):
    '''
    Function to read data from ultrasonic sensor
        Parameters:
            triggerPin (int): pin on the arduino connected to the sensor's trigger
            echoPin (int): pin on the arduino connected to the sensor's echo
            board: communication set-up with arduino
            ultrasonicData (list of integers): list of latest values (distances in cm) polled from the sensor
            predeterminedHeight (float): predetermined height of vehicle (cm)
        Returns:
            Function returns updated ultraSonicData
    '''

    board.set_pin_mode_sonar(triggerPin, echoPin, timeout=40000)
    vals = board.sonar_read(triggerPin)

   
    vehicleHeight = 28 - vals[0]

    if vehicleHeight >= 0:
        if vehicleHeight > predeterminedHeight:
            print("\n == ALERT: VEHICLE HEIGHT GREATER THAN PREDETERMINED HEIGHT ==")
            time.sleep(0.5)

        else:
            ultrasonicData.append(vehicleHeight)

    if len(ultrasonicData)==2:    
        ultrasonicData.pop(0)

        print(f'\nHeight of vehicle: {ultrasonicData}')

    elif vehicleHeight < 0:
        print("\n == NEGATIVE VEHICLE HEIGHT DETECED. CHECK ULTRASONIC SENSOR HEIGHT ==")
        time.sleep(0.5)

    time.sleep(0.5)


    return ultrasonicData

#create a function for LEDS, use while loop to keep it flashing for 6s
def flashing_leds(board):
    redLED = 9 #change the pin number accordingly
    yellowLED = 10
    
    flashingDuration = 6 

    startTime = time.time()
    endTime = startTime + flashingDuration

    while time.time() < endTime: #keep flashing the lights for 6s
        board.digital_write(redLED, 1) #just flash the red
        board.digital_write(yellowLED, 0)
        time.sleep(0.5)  

        board.digital_write(redLED, 0)
        board.digital_write(yellowLED, 1) #now yellow 
        time.sleep(0.5)  

    #turn off the lights when while loop is done
    board.digital_write(redLED, 0)
    board.digital_write(yellowLED, 0)

def main():
    board = pymata4.Pymata4()
    predeterminedHeight = 12
    ultrasonicData2 = []
    triggerPin2 = 7
    echoPin2 = 8

    while True:
        ultra_sonic(triggerPin2, echoPin2, board, ultrasonicData2, predeterminedHeight)

if __name__ == '__main__':
    main()
