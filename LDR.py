# Contains function to read data from the LDR
# Created By : Team A12: Nudara, Cooper, Devni, Kristian, Naailah
# Created Date: 15/05/2024
# version: 2.0

def read_LDR(pin, board):
    '''
    Function to read data from LDR
        Parameters:
            pin (int): analog pin to which the LDR is connected
            board: communication with the arduino

        Returns:
            Function returns 'night' or 'day' depending on LDR readings.
    '''

    # Specify the analog pin connected to the LDR
    board.set_pin_mode_analog_input(pin)

    # Read the analog value from the LDR
    ldrValue = board.analog_read(pin)

    print('Data from LDR: ', ldrValue[0])

    if ldrValue[0]>= 650:
        print("LDR indicates night time")
        return 'night'
    else:
        print("LDR indicates day time")
        return 'day'
        