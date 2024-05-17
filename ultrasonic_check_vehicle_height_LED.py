# Contains function to read vehicle height data from ultrasonic sensor
# Created By : Team A12: Nudara, Cooper, Devni, Kristian, Naailah
# Created Date: 14/05/2024
# version: 5.0

import time

def ultrasonic_height(triggerPin,echoPin,board,ultrasonicData, predeterminedHeight):
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

    if vehicleHeight > 0 and vehicleHeight != 28:
        ultrasonicData.append(vehicleHeight)
        if vehicleHeight > predeterminedHeight:
            print("== ALERT: VEHICLE HEIGHT GREATER THAN PREDETERMINED HEIGHT ==")
            flashing_leds(board)
    elif vehicleHeight < 0:
        print(f"== NEGATIVE VEHICLE HEIGHT DETECED: {vehicleHeight} cm. CHECK ULTRASONIC SENSOR HEIGHT ==")


    if len(ultrasonicData)==8:    
        ultrasonicData.pop(0)

    print(f'Height of vehicle: {ultrasonicData}')
    return ultrasonicData


def flashing_leds(board):
    '''
    Function to flash RGB red and yellow when vehicle height is greater than predetermined height
        Parameters:
            board: communication with arduino
        Returns:
            Function has no returns
    '''
    redPin = 3 #change the pin number accordingly
    greenPin = 4
    bluePin = 5

    board.set_pin_mode_digital_output(redPin)
    board.set_pin_mode_digital_output(greenPin)
    board.set_pin_mode_digital_output(bluePin)
    
    try:
        flashingDuration = 6 

        startTime = time.time() #can import the main loop time as a variable 
        endTime = startTime + flashingDuration

        while time.time() < endTime: #keep flashing the lights for 6s
            board.digital_write(redPin, 1) #just flash the red
            board.digital_write(greenPin, 0)
            board.digital_write(bluePin, 0)
            time.sleep(0.5)  

            board.digital_write(redPin, 1)
            board.digital_write(greenPin, 1) #now yellow 
            board.digital_write(bluePin, 0)
            time.sleep(0.5)  

        #turn off the lights when while loop is done
        board.digital_write(redPin, 0)
        board.digital_write(greenPin, 0)
        board.digital_write(bluePin, 0)
    except:
        board.digital_write(redPin, 0) #just flash the red
        board.digital_write(greenPin, 0)
        board.digital_write(bluePin, 0)

