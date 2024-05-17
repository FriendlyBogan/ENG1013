# Contains function to read data from ultrasonic sensor
# Created By : Team A12: Nudara, Cooper, Devni, Kristian, Naailah
# Created Date: 20/04/2024
# version: 5.0

def ultraSonic(triggerPin,echoPin,board,ultrasonicData, stage):
    '''
    Function to read data from ultrasonic sensor
        Parameters:
            triggerPin (int): pin on the arduino connected to the sensor's trigger
            echoPin (int): pin on the arduino connected to the sensor's echo
            board: communication set-up with arduino
            ultrasonicData (list of integers): list of latest values (distances in cm) polled from the sensor
        Returns:
            Function returns updated ultraSonicData
    '''

    board.set_pin_mode_sonar(triggerPin, echoPin, timeout=20000)
    vals = board.sonar_read(triggerPin)

    ultrasonicData.append((vals[0])) #only appending the distance

    if (len(ultrasonicData))>2:
        vel = round((ultrasonicData[-2]-ultrasonicData[-1])/(3),2)
        print(f'velocity = {vel}cm/sec')
        if vel> 10:
            print('Vehicle speed is over 10cm/s!, Alarms sound')
    
    if len(ultrasonicData)==8:    
        ultrasonicData.pop(0)

    print(f'\nData from Distance Ultrasonic Sensor: {ultrasonicData}')

    if stage == 'STG1' and len(ultrasonicData)>=3:
        if ultrasonicData[-1] == ultrasonicData[-2]:
            print('== Vehicle Distance has been constant for more than 3 seconds! ==')
    return ultrasonicData
  