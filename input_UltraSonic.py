from pymata4 import pymata4
import time 
board = pymata4.Pymata4()
triggerPin = 7
echoPin = 6
board.set_pin_mode_sonar(triggerPin,echoPin,timeout=200000) 
print(board.sonar_read(triggerPin))
