import time 
import math
from pymata4 import pymata4

board = pymata4.Pymata4()
board.set_pin_mode_sonar(9, 8, timeout=20000)
# time.sleep(5)
#TODO: time within loop and timing on data appending 

dddd=[]
tttt=[]

    vals=board.sonar_read(9)
    dddd.append(vals[0])
    tttt.append(round(vals[1],4))
    print(f'{dddd[-1]} cm and {tttt[-1]} sec')#only appending the distance
    time.sleep(1)
    if (len(dddd))!=1:

        print(f'velocity = {round((dddd[-1]-dddd[-2])/(tttt[-1]-tttt[-2]),2)}cm/sec\n')
#if time dif ttt[-1]-tttt[0]>20     pop first
