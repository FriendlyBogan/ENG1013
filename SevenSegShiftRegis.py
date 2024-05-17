# Contains functions to control and display message on the seven segment display
# Created By : Team A12: Nudara, Cooper, Devni, Kristian, Naailah
# Created Date: 19/04/2024
# version: 8.0

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

from pymata4 import pymata4
import time

digPins = [7,6,5,4]
RCLK = 9;  #latchPIN
SRCLK = 10; #clockPIN
SER = 8 #data 

def single_digit(board, binString):
    '''
    Function to display a single digit
        Parameters:
            board: communication with arduino
            binString (str): binary for the digit

        Returns:
            Function has no returns
    '''
    
    #first digit is decimal point
    turn_on = '11111110'
    turn_off = '00000000'
    binString = '0' + binString[::-1]

    for ch in binString:
        board.digital_write(SER, int(ch)) 
        board.digital_write(SRCLK, 1)
        board.digital_write(SRCLK, 0)

    board.digital_write(RCLK, 1)
    board.digital_write(RCLK, 0)

    time.sleep(0.00220)
    
    
    for ch in turn_off:
        board.digital_write(SER, int(ch)) 
        board.digital_write(SRCLK, 1)
        board.digital_write(SRCLK, 0)

    board.digital_write(RCLK, 1)
    board.digital_write(RCLK,0)

    time.sleep(0.00220)


def userinput_sevenseg():
    '''
    Function to obtain input from user.
        Parameters:
            Function has no parameters

        Returns:
            Function has no returns
    '''

    board = pymata4.Pymata4()
    sevenseg_pin_set_up(board)
    while True:
        try:
            print('--------------------------------------------------------------------------------')
            message = input("\nEnter a 4 digit alphanumeric message to display on the Seven Segment display: ")
            if len(message)<1 or len(message)>4:
                print("Invalid Message!")
                continue
            
            for ch in message:
                if ch not in lookUp.keys():
                    print(f'The character "{ch}", cannot be displayed!')
                    continue
            break
        except KeyboardInterrupt:
            break 

    display_sevenseg_inf(board, message)


def sevenseg_pin_set_up(board):
    '''
    Function to set up the pins on arduino
        Parameters:
            board: communication with arduino
        Returns:
            Function has no returns
    '''
    #setting up pin 
    board.set_pin_mode_digital_output(RCLK)
    board.set_pin_mode_digital_output(SRCLK)
    board.set_pin_mode_digital_output(SER)


    for pin in digPins:
        board.set_pin_mode_digital_output(pin)
        board.digital_write(pin,1)

        
def clear_display(board):
    '''
    Function to clear the display
        Parameters:
            board: communication with arduino
        Returns:
            Function has no returns
    '''
    for ch in '00000000':
        board.digital_write(SER, int(ch)) 
        board.digital_write(SRCLK, 1)
        board.digital_write(SRCLK, 0)

    board.digital_write(RCLK, 1)
    board.digital_write(RCLK,0)


def display_sevenseg_inf(board,message):
    '''
    Function to display all the digits infinitely till keyboard interrupt.
        Parameters:
            board: communication with arduino
            message(str): message to display

        Returns:
            Function has no returns
    '''

    digPins = [7,6,5,4]
    RCLK = 9;  #latchPIN
    SRCLK = 10; #clockPIN
    SER = 8 #data 

    #setting up pin 
    board.set_pin_mode_digital_output(RCLK)
    board.set_pin_mode_digital_output(SRCLK)
    board.set_pin_mode_digital_output(SER)
    print('Click on CTRL + C to exit!')

    for pin in digPins:
        board.set_pin_mode_digital_output(pin)
        board.digital_write(pin,1)


    while True:
        for i in range(len(message)):

            display_message = message

            try:
                for dig in range(len(display_message)):
                    print(dig)
                    board.digital_write(digPins[dig],0)
                    for x in lookUp.keys():
                        if x == display_message[dig]:
                            single_digit(board, lookUp[x])

                    board.digital_write(digPins[dig],1)


            except KeyboardInterrupt:

                for ch in '00000000':
                    board.digital_write(SER, int(ch)) 
                    board.digital_write(SRCLK, 1)
                    board.digital_write(SRCLK, 0)

                board.digital_write(RCLK, 1)
                board.digital_write(RCLK,0)
                quit()

