# Contains functions to control and display message on the seven segment display
# Created By : Team A12: Nudara, Cooper, Devni, Kristian, Naailah
# Created Date: 19/04/2024
# version: 6.0

from pymata4 import pymata4
import time

lookUp = {
    ' ': "0000000",
    '"': "0100010",
    '#': "0111111",
    '$': "1011011",
    '&': "0110001",
    "'": "0000010",
    '(': "1001010",
    ')': "1101000",
    '*': "1000010",
    '+': "0000111",
    "'": "0000100",
    '-': "0000001",
    '/': "0100101",
    '0': "1111110",
    '1': "0110000",
    '2': "1101101",
    '3': "1111001",
    '4': "0110011",
    '5': "1011011",
    '6': "1011111",
    '7': "1110000",
    '8': "1111111",
    '9': "1111011",
    ':': "1001000",
    ';': "1011000",
    '<': "1000011",
    '=': "0001001",
    '>': "1100001",
    '@': "1111101",
    'A': "1110111",
    'B': "0011111",
    'C': "1001110",
    'D': "0111101",
    'E': "1001111",
    'F': "1000111",
    'G': "1011110",
    'H': "0110111",
    'I': "0000110",
    'J': "0111100",
    'K': "1010111",
    'L': "0001110",
    'M': "1010100",
    'N': "1110110",
    'O': "1111110",
    'P': "1100111",
    'Q': "1101011",
    'R': "1100110",
    'S': "1011011",
    'T': "0001111",
    'U': "0111110",
    'V': "0111110",
    'W': "0101010",
    'X': "0110111",
    'Y': "0111011",
    'Z': "1101101",
    '[': "1001110",
    '\\': "0010011",
    ']': "1111000",
    '^': "1100010",
    '_': "0001000",
    '`': "0100000",
    'a': "1111101",
    'b': "0011111",
    'c': "0001101",
    'd': "0111101",
    'e': "1101111",
    'f': "1000111",
    'g': "1111011",
    'h': "0010111",
    'i': "0000100",
    'j': "0011000",
    'k': "1010111",
    'l': "0000110",
    'm': "0010100",
    'n': "0010101",
    'o': "0011101",
    'p': "1100111",
    'q': "1110011",
    'r': "0000101",
    's': "1011011",
    't': "0001111",
    'u': "0011100",
    'v': "0011100",
    'w': "0010100",
    'x': "0110111",
    'y': "0111011",
    'z': "1101101",
    '{': "0110001",
    '|': "0000110",
    '}': "0000111",
    '~': "1000000"
}

def write_all_digit(board, segPins,digPins, message,lookUpDict = lookUp):
    '''
    Function to display message on the seven segment display
        Parameters:
            board: communication set-up with arduino
            segPins (list of integers): A list consisting of the pins from arduino controlling the seven segments
            digPins (list of integers): A list consisting of the pins from arduino controlling the 4 digits
            message (str): message to be displayed
            lookUpDict (dict): consists of all characters that can be displayed and it corresponding binary values
        Returns:
            Function has no returns
    '''

    for pin in segPins:
        board.set_pin_mode_digital_message(pin)

    for dig in range(len(message)):
        board.set_pin_mode_digital_message(digPins[dig])
        board.digital_write(digPins[dig],1)

    while True:
        try:
            for dig in range(len(message)):
                board.digital_write(digPins[dig],0)
                for x in lookUpDict.keys():
                    if x == message[dig]:
                        for y in range(7):
                            board.set_pin_mode_digital_message(segPins[y])
                            board.digital_write(segPins[y],int(lookUpDict[x][y]))
                        for y in range(7):
                            board.digital_write(segPins[y],0)
                board.digital_write(digPins[dig],1)
        except KeyboardInterrupt:
            break
    
def start_seven_seg():
    '''
    Function which inputs and validates user message to be displayed on the seven segment
        Parameters:
            Function has no parameters.
        Returns:
            Function has no returns
    '''

    # define pins used by segments
    segPins = [3,4,5,6,7,8,9]
    digPins = [2,11,10,12]

    # initialise board
    board = pymata4.Pymata4()

    while True:

        while True:
            try:
                print('--------------------------------------------------------------------------------')
                message = input("\nEnter a 4 digit alphanumeric message to display on the Seven Segment display: ")
                if len(message)>4 or len(message)<1:
                    print("Invalid Message!")
                    continue
                
                for ch in message:
                    if ch not in lookUp.keys():
                        print(f'The character "{ch}", cannot be displayed!')
                        continue
                break
            except KeyboardInterrupt:
                break 
            
        write_all_digit(board, segPins,digPins, message,lookUp) 

        while True:
            rerun = input("Would you like to display another message? (Y/N): ").upper()

            if rerun not in ('Y', 'N'):
                print("Invalid input, try again!")
            else:
                break

        if rerun == 'Y':
            print("Clearing message...")
            time.sleep(3)
            continue
        elif rerun == 'N':
            # shutdown the board
            print("Clearing message...")
            time.sleep(3)
            break
  