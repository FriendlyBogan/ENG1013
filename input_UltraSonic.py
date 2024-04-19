
def ultraSonic(triggerPin,echoPin):
    from pymata4 import pymata4
    import time 
    import math
    board = pymata4.Pymata4()
    board.set_pin_mode_sonar(triggerPin,echoPin,timeout=150000) 
    ultrasonicData = []
    intialDistance =''
    finalDistance =''
    initialData = []
    speedingAlarm = False
    try:
        t0 = time.time()
        while True:
            #TODO: time within loop and timing on data appending 
            timeInLoop = time.time()
            ultrasonicData.append((board.sonar_read(triggerPin)[0])) #only appending the distance
            time.sleep(1) #trial error indicates that the time to append data at 1Hz is better than the slower ones. 
            timeElapsed = timeInLoop - t0
            if 1 <timeElapsed <= 3:
                intialDistance = int(ultrasonicData[1])/100
            if len(ultrasonicData) > 7: #assuming the data needed for the graphing is at 7 index long, able to change 
                ultrasonicData.pop(0)
            if  timeElapsed >= 10:
                finalDistance = int(ultrasonicData[6])/100
            try:
                if intialDistance != '' and finalDistance != '':
                    speed = math.floor((intialDistance - finalDistance) / timeElapsed,3)
                    if speed > 0.0210: #trial but please experiment this aswell 
                        print("CAR IS SPEEDING")
                        speedingAlarm = True
                    quit()
            except ValueError:
                InvalidInput = input("invalid distance try again? (Y/N)")
                if InvalidInput == "Y":
                    print("restarting loop")
                    continue
                if InvalidInput == "N":
                    print('exiting loop')
                    quit()
    except KeyboardInterrupt:
        print("user interruption")
        quit()
            