
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
  
            