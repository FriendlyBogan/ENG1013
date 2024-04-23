import time 
from pymata4 import pymata4
def pedPresense(pin,board,pedcount,pedPresense):
#TODO: def this as a function with parameter = analog pin, flesh out program if needed
    board.set_pin_mode_analog_input(pin)
    try:
        while True:
            value = board.analog_read(pin)
            if value[0] == 0:
                pedPresense = True
                pedcount += 1
    except KeyboardInterrupt:
            board.shutdown()
        