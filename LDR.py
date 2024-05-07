from pymata4 import pymata4
import time

def read_LDR(pin, board):
    # Specify the analog pin connected to the LDR
    ldr_pin = 0  # Assuming the LDR is connected to analog pin A0
    board.set_pin_mode_analog_input(0)

    try:

        # Read the analog value from the LDR
        ldr_value = board.analog_read(ldr_pin)

        print('Data from LDR: ', ldr_value[0])

        if ldr_value[0]>= 900:
            return 'night'
        else:
            return 'day'
        

    except KeyboardInterrupt:
        # Clean up when the program is interrupted
        board.close()