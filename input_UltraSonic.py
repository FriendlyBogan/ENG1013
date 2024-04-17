def ultraSonic(triggerPin,echoPin):
    from pymata4 import pymata4
    import time 
    board = pymata4.Pymata4()
    board.set_pin_mode_sonar(triggerPin,echoPin,timeout=150000) 
    ultrasonicData = []
    while True:
        ultrasonicData.append((board.sonar_read(triggerPin)[0])) #only appending the distance
        t0 = time.time()
        time.sleep(1) #trial error indicates that the time to append data at 1Hz is better than the slower ones. 
        initalDistance = ultrasonicData[1] # the 0th index is always so not valid, trial error finds that first index is better
        if len(ultrasonicData) > 7: #assuming the data needed for the graphing is at 7 index long, able to change 
            ultrasonicData.pop(0)
        if time.time() - t0 == 10: #setting runtime = 10 seconds
            return ultrasonicData
            quit()
            