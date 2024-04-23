import time 
from pymata4 import pymata4
def pedPresense(pin,board,pedcount,pedPresense):
    board.set_pin_mode_digital_input(pin)
    try:
        while True:
            value = board.digital_read(pin)
            if value[0] == 0:
                pedPresense = True
                pedcount += 1
                time.sleep(1) #adding a sleep so it doesnt overflow data 
                print(pedcount)
                print(pedPresense)
    except KeyboardInterrupt:
            board.shutdown()