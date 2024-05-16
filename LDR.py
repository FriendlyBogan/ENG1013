from pymata4 import pymata4
import time

def read_LDR(pin, board):
    # Specify the analog pin connected to the LDR
    ldr_pin = 0  # Assuming the LDR is connected to analog pin A0
    board.set_pin_mode_analog_input(pin)


    # Read the analog value from the LDR
    ldr_value = board.analog_read(pin)

    print('Data from LDR: ', ldr_value[0])

    if ldr_value[0]>= 650:
        print("LDR indicates night time")
        return 'night'
    else:
        print("LDR indicates day time")
        return 'day'
        