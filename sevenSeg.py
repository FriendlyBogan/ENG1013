# import pymata4, time
from pymata4 import pymata4
import time
# note for number pins to turn ON is setting the signal to LOW (0)
# for alphabets is to turn ON is HIGH (1)
# function to write data to the first digit of the 7-seg


# initialsing all digits to be empty so it can be repopulated later on demand 
d1 = '' #pin12
d2 = '' #pin9
d3 = '' #pin8
d4 = '' #pin6
"when any pin 12,9,8,6 is closed that mean the digit is ON if want OFF then dont close the circuit (dont connect to GND)"

number = input("what is the number? ")

def write_first_digit(board, segPins, number):
    # TODO: find dictionary for the 
    lookUp = {
    0: 0b01111110,
    1: 0b00110000,
    2: 0b01101101,
    3: 0b01111001,
    4: 0b00110011,
    5: 0b01011011,
    6: 0b01011111,
    7: 0b01110000,
    8: 0b01111111,
    9: 0b01111011,

    ' ': 0b00000000,
    '!': 0b10110000,
    '"': 0b00100010,
    '#': 0b00111111,
    '$': 0b01011011,
    '%': 0b10100101,
    '&': 0b00110001,
    "'": 0b00000010,
    '(': 0b01001010,
    ')': 0b01101000,
    '*': 0b01000010,
    '+': 0b00000111,
    "'": 0b00000100,
    '-': 0b00000001,
    '.': 0b10000000,
    '/': 0b00100101,
    '0': 0b01111110,
    '1': 0b00110000,
    '2': 0b01101101,
    '3': 0b01111001,
    '4': 0b00110011,
    '5': 0b01011011,
    '6': 0b01011111,
    '7': 0b01110000,
    '8': 0b01111111,
    '9': 0b01111011,
    ':': 0b01001000,
    ';': 0b01011000,
    '<': 0b01000011,
    '=': 0b00001001,
    '>': 0b01100001,
    '?': 0b11100101,
    '@': 0b01111101,
    'A': 0b01110111,
    'B': 0b00011111,
    'C': 0b01001110,
    'D': 0b00111101,
    'E': 0b01001111,
    'F': 0b01000111,
    'G': 0b01011110,
    'H': 0b00110111,
    'I': 0b00000110,
    'J': 0b00111100,
    'K': 0b01010111,
    'L': 0b00001110,
    'M': 0b01010100,
    'N': 0b01110110,
    'O': 0b01111110,
    'P': 0b01100111,
    'Q': 0b01101011,
    'R': 0b01100110,
    'S': 0b01011011,
    'T': 0b00001111,
    'U': 0b00111110,
    'V': 0b00111110,
    'W': 0b00101010,
    'X': 0b00110111,
    'Y': 0b00111011,
    'Z': 0b01101101,
    '[': 0b01001110,
    '\\': 0b00010011,
    ']': 0b01111000,
    '^': 0b01100010,
    '_': 0b00001000,
    '`': 0b00100000,
    'a': 0b01111101,
    'b': 0b00011111,
    'c': 0b00001101,
    'd': 0b00111101,
    'e': 0b01101111,
    'f': 0b01000111,
    'g': 0b01111011,
    'h': 0b00010111,
    'i': 0b00000100,
    'j': 0b00011000,
    'k': 0b01010111,
    'l': 0b00000110,
    'm': 0b00010100,
    'n': 0b00010101,
    'o': 0b00011101,
    'p': 0b01100111,
    'q': 0b01110011,
    'r': 0b00000101,
    's': 0b01011011,
    't': 0b00001111,
    'u': 0b00011100,
    'v': 0b00011100,
    'w': 0b00010100,
    'x': 0b00110111,
    'y': 0b00111011,
    'z': 0b01101101,
    '{': 0b00110001,
    '|': 0b00000110,
    '}': 0b00000111,
    '~': 0b01000000
}

    for pin in segPins:
        board.set_pin_mode_digital_output(pin)
    # TODO: write the appropriate output for the provided number
    for x in lookUp.keys():
        if x == number:
            for y in range(7): #TODO: change this to work for all pins that are needed # this is addressing to all the pins for the number pin in arduino 
                board.digital_write(segPins[y],int(lookUp[x][y])) #x is the key in dict and y is the pin 
 
 
# Main function
def main():
    # define pins used by segments
    segPins = [3,4,5,6,7,8,9]
    # initialise board
    board = pymata4.Pymata4()
    # set up pins for digital output
    for pin in segPins:
        board.set_pin_mode_digital_output(pin)
    # Call function write_first_digit
    write_first_digit(board, segPins, 3)
    time.sleep(1)
    write_first_digit(board, segPins, 4)
    time.sleep(1)
    write_first_digit(board, segPins, 2)
    time.sleep(1)
    write_first_digit(board, segPins, 1)
    # wait 5 seconds
    time.sleep(5)      
    # shutdown the board
    board.shutdown()
 
if __name__ == "__main__":
    main() 