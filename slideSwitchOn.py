# Contains function to read the state of the slide switch
# Created By : Team A12: Nudara, Cooper, Devni, Kristian, Naailah
# Created Date: 15/05/2024
# version: 1.0

def slide_switch_on(board, pin):
    '''
    Function to read the state of the slide switch
        Parameters:
            board: communication with arduino
            pin (int): pin number on arduino to which the switch is connected
        Returns:
            returns True or False
    '''

    board.set_pin_mode_digital_input(pin)
    
    if board.digital_read(pin)[0] == 1:
        return True
    else:
        return False

