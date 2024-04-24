from pymata4 import pymata4
import time
board = pymata4.Pymata4()

RCLK = 9;  #latchPIN
SRCLK = 10; #clockPIN
SER = 8; #data !!DOUBLE CHECK IF THE PINS ARE RIGHT!!
msg_raw = str(01111111)
msg = msg_raw
msg = msg.split()
#set the pins to the board as an output
board.set_pin_mode_digital_output(RCLK)
board.set_pin_mode_digital_output(SRCLK)
board.set_pin_mode_digital_output(SER)





#turning on each LEDs
def LED1 (stat):
    board.digital_write(RCLK,0)
    board.digital_write(SER,stat) #if ser is 0 is on, 1 is off 
    board.digital_write(SRCLK,1)

def LED2 (stat):
    board.digital_write(RCLK,0)
    board.digital_write(SER,stat) #if ser is 0 is on, 1 is off 
    board.digital_write(SRCLK,1)

def LED3 (stat):
    board.digital_write(RCLK,0)
    board.digital_write(SER,stat) #if ser is 0 is on, 1 is off 
    board.digital_write(SRCLK,1)

def LED4 (stat):
    board.digital_write(RCLK,0)
    board.digital_write(SER,stat) #if ser is 0 is on, 1 is off 
    board.digital_write(SRCLK,1)


def LED5 (stat):
    board.digital_write(RCLK,0)
    board.digital_write(SER,stat) #if ser is 0 is on, 1 is off 
    board.digital_write(SRCLK,1)


def LED6 (stat):
    board.digital_write(RCLK,0)
    board.digital_write(SER,stat) #if ser is 0 is on, 1 is off 
    board.digital_write(SRCLK,1)


def LED7 (stat):
    board.digital_write(RCLK,0)
    board.digital_write(SER,stat) #if ser is 0 is on, 1 is off 
    board.digital_write(SRCLK,1)


def LED8 (stat):
    board.digital_write(RCLK,0)
    board.digital_write(SER,stat) #if ser is 0 is on, 1 is off 
    board.digital_write(SRCLK,1)
    board.digital_write(RCLK,1)

for char, _ in zip(msg, range(len(msg))):
    LED1(char)
    LED2(char)
    LED3(char)
    LED4(char)
    LED5(char)
    LED6(char)
    LED7(char)
    LED8(char)


    

