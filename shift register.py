from pymata4 import pymata4
import time
board = pymata4.Pymata4()
MSBFIRST = pymata4.Pymata4().MSBFIRST

RCLK = 12;  #latchPIN
SRCLK = 11; #clockPIN
SER = 14; #data !!DOUBLE CHECK IF THE PINS ARE RIGHT!!
msg = 10000000
#set the pins to the board as an output
board.set_pin_mode_digital_output(RCLK)
board.set_pin_mode_digital_output(SRCLK)
board.set_pin_mode_digital_output(SER)

#for i in len(msg):
msg = msg.split()
digits = msg[i]


#make a function with the shift register process
#make the SR low, to get the data in. connect with the board since it has the pin data
#def shift_register_process(byte_config):
board.digital_write(RCLK,0)
board.digital_write(SER,1)
board.digital_write(SRCLK,1)
board.digital_write(RCLK,1)


#function to account for all colour light changes
#def color_light_changes():
