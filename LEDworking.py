def lights(stage):

    if stage == "1":
        ON = "10000101"[::-1]
    if stage == "2":
        ON = "01000101"[::-1]
    if stage == "3":
        ON = "00100101"[::-1]
    if stage == "4":
        ON = "00110010"[::-1]
    if stage == "5":
        ON = "00101010"[::-1]
    if stage == "6":
        ON = "00100101"[::-1]
    

    from pymata4 import pymata4
    import time
    board = pymata4.Pymata4()

    RCLK = 9;  #latchPIN
    SRCLK = 10; #clockPIN
    SER = 8; #data !!DOUBLE CHECK IF THE PINS ARE RIGHT!!

    ON = "01000010"[::-1]
    ON_list = [char for char in ON]
    #set the pins to the board as an output
    board.set_pin_mode_digital_output(RCLK)
    board.set_pin_mode_digital_output(SRCLK)
    board.set_pin_mode_digital_output(SER)



    #turning on each LEDs
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

    def LED8 (stat):
        board.digital_write(SER,stat) #if ser is 0 is on, 1 is off 
        board.digital_write(SRCLK,1)
        board.digital_write(SRCLK,0)
        board.digital_write(RCLK,1)
        board.digital_write(RCLK,0)
    
    def stage5(stat):
        startingStage5 = time.time()
        board.digital_write(SER,stat) #if ser is 0 is on, 1 is off 
        board.digital_write(SRCLK,1)
        board.digital_write(SRCLK,0)
        while time.time() - startingStage5 < 3:
            board.digital_write(RCLK,1)
            time.sleep(0.25)
            board.digital_write(RCLK,0)
        



    def LED(digits): 
        ledList = [LED1, LED2, LED3, LED4, LED5, LED6, LED7, LED8]
        ledStage5 = [LED1, LED2, LED3, LED4, LED5,LED6,stage5, LED8]
        if stage == "5":
            for ledFunc, flash in zip(ledList, digits):
            flash =  int(flash)
            ledFunc(digit)
        for ledFunc, digit in zip(ledList, digits):
            digit = int(digit)
            ledFunc(digit)
