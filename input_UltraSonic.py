'''
def ultraSonic(triggerPin,echoPin,board,ultrasonicData):
    
    import time 
    import math
     
    intialDistance =''
    finalDistance =''
    sleepTime = 0.25
   

    #TODO: time within loop and timing on data appending 
    ultrasonicData.append((board.sonar_read(triggerPin)[0])) #only appending the distance

    if len(ultrasonicData) >= 2:
        intialDistance = ultrasonicData[-2]
        finalDistance = ultrasonicData[-1]

    if intialDistance != '' and finalDistance != '':
            speed = round(((intialDistance/100) - (finalDistance/100)) / 2,3)
            if speed > 0.28: #trial but please experiment this aswell 
                print("CAR IS SPEEDING")
                speedingAlarm = True
                print("Vehicle is Speeding!")

    return ultrasonicData
'''

def ultraSonic(triggerPin,echoPin,board,ultrasonicData):

    board.set_pin_mode_sonar(triggerPin, echoPin, timeout=20000)
    # time.sleep(5)
    #TODO: time within loop and timing on data appending 


    timelist=[]

    vals=board.sonar_read(triggerPin)

    ultrasonicData.append((vals[0])) #only appending the distance
    timelist.append(round(vals[1],4))
    print(f'\n{ultrasonicData}')
    if (len(ultrasonicData))>2:
        print(f'velocity = {round((ultrasonicData[-1]-ultrasonicData[-2])/(3),2)}cm/sec')
    if len(ultrasonicData)>7:    
        ultrasonicData.pop(0)

    #TODO: time within loop and timing on data appending 
    return ultrasonicData
  
            