# Contains function to detect pedestrian presence
# Created By : Team A12: Nudara, Cooper, Devni, Kristian, Naailah
# Created Date: 20/04/2024
# version: 3.0

def ped_presence(pin,board,pedCount):
    '''
    Function to detect pedestrian presence
        Parameters:
            pin (int): input pin on the arduino
            board: communication set-up with arduino
            pedCount (int): counter for number of button presses
        Returns:
            Function has no returns
    '''
       
    board.set_pin_mode_digital_input(pin)
    try:
        value = board.digital_read(pin)
        if value[0] == 0:
            pedCount += 1
            if pedCount > 0:
                print('BUTTON HAS BEEN PRESSED!')
        return pedCount
    except KeyboardInterrupt:
        pass