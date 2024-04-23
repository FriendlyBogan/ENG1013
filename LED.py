from pymata4 import pymata4
board = pymata4.Pymata4()
msg = [1111111,00000000,11111111,00000000,11111111,00000000,11111111,00000000]
#initalising pin and setting pins to correct mode
ser = board.set_pin_mode_digital_input(8)
STCP = board.set_pin_mode_digital_input(9)
SHCP = board.set_pin_mode_digital_input(10)

board.digital_pin_write(SHCP,0)

for i in range(1,8,1):
    board.digital_pin_write(STCP,0)
    board.digital_pin_write(ser,msg[i])
    board.digital_pin_write(STCP,1)

board.digital_pin_write(SHCP,1)




    