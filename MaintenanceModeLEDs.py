import time
from pymata4 import pymata4

board = pymata4.Pymata4()  

def maintenance_lights(RCLK, SRCLK, SER, board):
    """
    Function to control the functionality of the LEDs.
    Parameters:
        board: communication set-up with Arduino.
    Returns:
        None
    """

    # Setting up pins
    board.set_pin_mode_digital_output(RCLK)
    board.set_pin_mode_digital_output(SRCLK)
    board.set_pin_mode_digital_output(SER)
    
    while True:
        try:
            # Turn on LEDs
            board.digital_write(SER, 0)
            board.digital_write(SRCLK, 1)
            board.digital_write(SRCLK, 0)

            board.digital_write(SER, 0)
            board.digital_write(SRCLK, 1)
            board.digital_write(SRCLK, 0)

            board.digital_write(SER, 0)
            board.digital_write(SRCLK, 1)
            board.digital_write(SRCLK, 0)

            board.digital_write(SER, 1)
            board.digital_write(SRCLK, 1)
            board.digital_write(SRCLK, 0)

            board.digital_write(SER, 0)
            board.digital_write(SRCLK, 1)
            board.digital_write(SRCLK, 0)

            board.digital_write(SER, 0)
            board.digital_write(SRCLK, 1)
            board.digital_write(SRCLK, 0)

            board.digital_write(SER, 1)
            board.digital_write(SRCLK, 1)
            board.digital_write(SRCLK, 0)

            board.digital_write(SER, 0)
            board.digital_write(SRCLK, 1)
            board.digital_write(SRCLK, 0)
            board.digital_write(RCLK, 1)
            board.digital_write(RCLK, 0)

            time.sleep(0.5)

            
            board.digital_write(SER, 0)

            board.digital_write(SRCLK, 1)
            board.digital_write(SRCLK, 0)

            board.digital_write(SRCLK, 1)
            board.digital_write(SRCLK, 0)

            board.digital_write(SRCLK, 1)
            board.digital_write(SRCLK, 0)

            board.digital_write(SRCLK, 1)
            board.digital_write(SRCLK, 0)

            board.digital_write(SRCLK, 1)
            board.digital_write(SRCLK, 0)

            board.digital_write(SRCLK, 1)
            board.digital_write(SRCLK, 0)

            board.digital_write(SRCLK, 1)
            board.digital_write(SRCLK, 0)

            board.digital_write(SRCLK, 1)
            board.digital_write(SRCLK, 0)

            board.digital_write(RCLK, 1)
            board.digital_write(RCLK, 0)

            time.sleep(0.5)

        except KeyboardInterrupt:
            board.shutdown()

def main():
    maintenance_lights(board)

if __name__ == "__main__":
    main()
