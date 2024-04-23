
def ultraSonic(triggerPin,echoPin,board,ultrasonicData):
    
    import time 
    import math

    from pymata4 import pymata4

    board = pymata4.Pymata4()
    board.set_pin_mode_sonar(9, 8, timeout=20000)
    # time.sleep(5)
    #TODO: time within loop and timing on data appending 

    distancelist=[]
    timelist=[]

    vals=board.sonar_read(triggerPin)
    distancelist.append(vals[0])
    timelist.append(round(vals[1],4))
    print(f'{distancelist[-1]} cm and {timelist[-1]} sec')#only appending the distance
    time.sleep(1)
    if (len(distancelist))!=1:
        print(f'velocity = {round((distancelist[-1]-distancelist[-2])/(timelist[-1]-timelist[-2]),2)}cm/sec\n')
    if timelist[-1]-timelist[0]>20:    
        distancelist.pop[0] 

    #TODO: time within loop and timing on data appending 
    ultrasonicData.append((board.sonar_read(triggerPin)[0])) #only appending the distance

    return ultrasonicData






