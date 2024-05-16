import math


def thermistor(board, dataList):

    analog_pin = 1
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
        dataList.append(temp)

    if len(dataList) > 7:
        dataList.pop(0)
    return dataList

'''         
def main():
    while True:
        thermistor(board, stage=0)

if __name__ == '__main__':
    main()
'''