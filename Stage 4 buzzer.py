from pymata4 import pymata4
import time

def stage_four_buzzer_day(board):
    buzzer4Pin = 3  # Or any available PWM Pin
    board.set_pin_mode_pwm_output(buzzer4Pin)

    stageFourDurationDay = 30  # thats how long stage 4 is @ daytime
    startTime = time.time()

    while time.time() - startTime < stageFourDurationDay: 
        board.digital_write(buzzer4Pin, 1)
        time.sleep(0.5)  # on for 0.5s
        board.digital_write(buzzer4Pin, 0)
        time.sleep(0.5)  # off for 0.5s

def stage_four_buzzer_night(board):
    buzzer4Pin = 3  # Or any available PWM Pin
    board.set_pin_mode_pwm_output(buzzer4Pin)

    stageFourDurationNight = 10  # thats how long stage 4 is @ nighttime
    startTime = time.time()

    while time.time() - startTime < stageFourDurationNight: 
        board.digital_write(buzzer4Pin, 1)
        time.sleep(0.5)  # on for 0.5s
        board.digital_write(buzzer4Pin, 0)
        time.sleep(0.5)  # off for 0.5s

