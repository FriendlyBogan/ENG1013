from pymata4 import pymata4
import time
import math

board = pymata4.Pymata4()
analog_pin = 0
board.set_pin_mode_analog_input(0)
digital_pin = 8
board.set_pin_mode_digital_input(digital_pin)

def thermistor(board, stage):

    value, timeStamp = board.analog_read(0)
    analogVOut = float(value)
    vIn = 5
    resistor1 = 10000
    vOut = analogVOut * (5/1023)

    try:
        if vOut == 0:
            print('Checking values . . .')
            time.sleep(1)
            pass
        else:
            resistor2 = (vOut * resistor1) / (vIn - vOut)
            thermistorValue = resistor2/1000
            temp = round(-21.21 * math.log1p(thermistorValue) + 72.203,2)
            print('Current Temperature:', temp, '°C')
            time.sleep(1)

    except KeyboardInterrupt:
        board.shutdown()
        
    if stage == 'stageOne':
        if temp > 35:
            stage_time += 5
            print('\n == TEMP EXCEEDED 35°C. INCREASING STAGE TIMING BY 5 SECONDS ==')
    if stage == 'stageFour':
        if temp > 35:
            stage_time += 5
            print('\n == TEMP EXCEEDED 35°C. INCREASING STAGE TIMING BY 5 SECONDS ==')
            
def main():
    while True:
        thermistor(board, stage=0)

if __name__ == '__main__':
    main()