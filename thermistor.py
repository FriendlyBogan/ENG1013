# Contains functions to read temperature data from thermistor
# Created By : Team A12: Nudara, Cooper, Devni, Kristian, Naailah
# Created Date: 10/05/2024
# version: 4.0

import math

def thermistor(board, dataList):
    '''
    Function to display a single digit
        Parameters:
            board: communication with arduino
            dataList(list of floats): list of latest values (temperatures in degree C) polled from thermistor
        Returns:
            returns updated dataList
    '''

    board.set_pin_mode_analog_input(1)

    value, timeStamp = board.analog_read(1)
    analogVOut = float(value)
    vIn = 5
    resistor1 = 10000
    vOut = analogVOut * (5/1023)

    
    if vOut == 0:
        print('Checking values from thermistor. . .')
        pass
    else:
        resistor2 = (vOut * resistor1) / (vIn - vOut)
        thermistorValue = resistor2/1000
        temp = round(-21.21 * math.log1p(thermistorValue) + 72.203,2)
        print('Current Temperature:', temp, '°C')
        if temp<51 and temp>-3:
            dataList.append(temp)

    if len(dataList) > 7:
        dataList.pop(0)
    return dataList
