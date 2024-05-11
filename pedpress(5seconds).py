# Contains function to detect pedestrian presence
# Created By : Team A12: Nudara, Cooper, Devni, Kristian, Naailah
# Created Date: 20/04/2024
# version: 2.0

def pedPresence(pin,board,pedCount,stage,timeLeft):

    '''
    Function to detect pedestrian presence
        Parameters:
            pin (int): input pin on the arduino
            board: communication set-up with arduino
            pedcount: counter for number of button presses
            stage (str): current stage of the traffic sequence
            timeLeft (int): time left in current stage of traffic sequence
        Returns:
            Int: updated pedcount if pedestrian push
              button is pressed, otherwise returns original pedcount
    '''

    board.set_pin_mode_digital_input(pin)
    try:
        value = board.digital_read(pin)
        if value[0] == 0:
            if stage == 'Stage One':
                 # Reduces the time left to a maximum of 5 seconds
                 timeLeft = min(5, timeLeft)
            pedCount += 1
        return pedCount, timeLeft
    except KeyboardInterrupt:
            board.shutdown()