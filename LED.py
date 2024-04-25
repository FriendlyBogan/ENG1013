def lights(stage):    
    from pymata4 import pymata4
    import time
    board = pymata4.Pymata4()
    RCLK = 9;  #latchPIN
    SRCLK = 10; #clockPIN
    SER = 8 #data 
    GND = 11; #GNDPin

    if stage == 1:
        ON = "10000101"[::-1]
    if stage == 2:
        ON = "01000101"[::-1]
    if stage == 3:
        ON = "00100101"[::-1]
    if stage == 4:
        ON = "00110010"[::-1]
    if stage == 5:
        ON = "00101010"[::-1]
    if stage == 6:
        ON = "00100101"[::-1]
    

    OnList = [char for char in ON] #seperate each bit as an element and store it within a list 

    #setting up pin 
    board.set_pin_mode_digital_output(RCLK)
    board.set_pin_mode_digital_output(SRCLK)
    board.set_pin_mode_digital_output(SER)
    board.set_pin_mode_digital_output(GND) #this will only be used for led7 during stage 5


    #function to turn on each LEDs
    def LED1 (stat):
        board.digital_write(RCLK,0)
        board.digital_write(SER,stat) #if ser is 0 is on, 1 is off 
        board.digital_write(SRCLK,1)
        board.digital_write(SRCLK,0)

    def LED2 (stat):
        board.digital_write(SER,stat) #if ser is 0 is on, 1 is off 
        board.digital_write(SRCLK,1)
        board.digital_write(SRCLK,0)

    def LED3 (stat):
        board.digital_write(SER,stat) #if ser is 0 is on, 1 is off 
        board.digital_write(SRCLK,1)
        board.digital_write(SRCLK,0)

    def LED4 (stat):
        board.digital_write(SER,stat) #if ser is 0 is on, 1 is off 
        board.digital_write(SRCLK,1)
        board.digital_write(SRCLK,0)


    def LED5 (stat):
        board.digital_write(SER,stat) #if ser is 0 is on, 1 is off 
        board.digital_write(SRCLK,1)
        board.digital_write(SRCLK,0)


    def LED6 (stat):
        board.digital_write(SER,stat) #if ser is 0 is on, 1 is off 
        board.digital_write(SRCLK,1)
        board.digital_write(SRCLK,0)

    def LED7 (stat):
        board.digital_write(SER,stat) #if ser is 0 is on, 1 is off 
        board.digital_write(SRCLK,1)
        board.digital_write(SRCLK,0)
        if stage == 5:
            board.digital_write(GND,0)
            time.sleep(0.5)
            board.digital_write(GND,1)
            time.sleep(0.5)
            board.digital_write(GND,0)
            time.sleep(0.5)
            board.digital_write(GND,1)
            time.sleep(0.5)
            board.digital_write(GND,0)
            time.sleep(0.5)
            board.digital_write(GND,1)

    def LED8 (stat):
        board.digital_write(SER,stat) #if ser is 0 is on, 1 is off 
        board.digital_write(SRCLK,1)
        board.digital_write(SRCLK,0)
        board.digital_write(RCLK,1)
        board.digital_write(RCLK,0)
    
    #Looping thru each LED functions with its own bit of information for that stage 
    ledList = [LED1, LED2, LED3, LED4, LED5, LED6, LED7, LED8]
    for ledFunc, digit in zip(ledList, OnList): #zip is used here so that both list can iterate at the same time
        digit = int(digit)
        ledFunc(digit)


