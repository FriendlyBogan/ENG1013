# Complete code for Milestone 3
# Created By : Team A12: Nudara, Cooper, Devni, Kristian, Naailah
# Created Date: 01/04/2024
# version: 18.0

import time
from pymata4 import pymata4
from input_ultraSonic import ultraSonic
from graphing import graphing_distance, graphing_height, graphing_temperature
from pedpress import ped_presence
from SevenSegShiftRegis import userinput_sevenseg
from LDR import read_LDR
from ultrasonic_check_vehicle_height_LED import ultrasonic_height
from thermistor import thermistor
from slideSwitchOn import slide_switch_on


def display_main_menu(username, userParameters, polledData, polledData2, thermistorList,predeterminedHeight, board,blockedTime):
    """
    Used to display the main menu.
        Parameters:
            username (str): username of user currently operating the system.
            userParameters (dict): contains a dictionary of stored user profiles.
            polledData (list of integers): list of latest values (distances in cm) polled from the sensor
            polledData2 (list of integers): list of latest values (heights in cm) polled from the sensor
            thermistorList (list of floats): list of latest values (temperatures in degree C) polled from thermistor
            predeterminedHeight (int): height limit of vehicles
            board: communication set-up with arduino
            blockedTime (int): time for which the user is blocked from maintenance mode
        Returns:
            username (str): username of user currently operating the system.
            userParameters (dict): contains a dictionary of stored user profiles.
            polledData (list): list of latest values (distances in cm) polled from the sensor
            polledData2 (list of integers): list of latest values (heights in cm) polled from the sensor
            thermistorList (list of floats): list of latest values (temperatures in degree C) polled from thermistor
            predeterminedHeight (int): height limit of vehicles
            blockedTime (int): time for which the user is blocked from maintenance mode

    """
    print("\n=== Main Menu ===\n")
    print("1: Normal Mode")
    print("2: Maintenance Adjustment Mode")
    print("3: Data Observation Mode")
    print("0. Quit the program\n")

    # variable to hold choice (starting value is invalid)
    choice = -1 
    # Wait for input
    while True:
        try:
            choice = int(input("Option: "))
            if choice in [0, 1, 2, 3]:
                break
            else:
                print("Error: Invalid option")
        except ValueError:
            print("Error: Only numbers are accepted")

    # Process choice
    if choice == 1:
        polledData, polledData2, thermistorList = normal_mode(username, userParameters, polledData, polledData2,thermistorList, predeterminedHeight, board)
    elif choice == 2:
        userParameters, blockedTime = authorize_user(username, userParameters, blockedTime, predeterminedHeight)
    elif choice == 3:
        display_data_observation_menu(polledData, polledData2, thermistorList)
    elif choice == 0:
        print("Shutting the system down...")
        board.shutdown()
        quit()

    return username, userParameters, polledData,polledData2,thermistorList, predeterminedHeight, blockedTime

def authorize_user(username, userParameters, blockedTime, predeterminedHeight):
    '''
    Used to authorize user to access the Maintenance Adjustment settings
        Parameters:
            username (str): stores username of profile.
            userParameters (dict): contains a dictionary of stored user profiles.
            authorization (str): determines whether user is allowed access to maintenance adjustment mode
            blockedTime (int): time for which the user is blocked from maintenance mode
            predeterminedHeight (int): height limit of vehicles
        Returns:
            Function returns updated userParameters and blockedTime
    '''

    if time.time()>blockedTime or blockedTime == 0 :

        while True:
            try:
                decision = input("\nDo you want to create a new user profile? (Y/N): ")
                decision = decision.upper() # so if the user inputs Y or y, either way the input is accepted
                if decision == 'Y':
                    username = input("\nEnter your username: ")
                    if username not in userParameters:
                        print("\nCreating new user profile...")
                        pin = input("Set your PIN: ")
                        userParameters[username] = {
                            'pin': pin,
                            'predeterminedHeight': predeterminedHeight,
                            'distanceRange': 15
                        }
                        print("Profile created successfully!")
                    else:
                        print('Username already exists!')
                    return userParameters, blockedTime
                elif decision == 'N':
                    subsequentProfile = input("Do you already have a profile (Y/N)? ")
                    subsequentProfile = subsequentProfile.upper() # so if the user inputs Y/y, N/n - either way the input is accepted
                    if subsequentProfile == 'Y':
                        username = input("\nEnter your username: ")
                        if username not in userParameters:
                            print("Error. User not found")
                            time.sleep(1)
                        else:
                            break
                    elif subsequentProfile == 'N':
                        print("\nGoing back to main menu...")
                        time.sleep(1)
                        return userParameters, blockedTime
                    elif decision != 'Y' or 'N':
                        print("Please enter Y or N.")
                elif decision != 'Y' or 'N':
                    print("Please enter Y or N.")
            except KeyboardInterrupt:
                print("\nGoing back to main menu...") # handling for wanting to go back to main menu anywhere in the loop
                time.sleep(1)
                return userParameters,blockedTime

        #ask for PIN, 3 times max, then return to main menu (Lock person out of system settings) (for maintenace adjustment mode)
        for tries in range(3):
            userPin = input('\nEnter PIN: ')
            if userPin == userParameters[username]['pin']:
                print("PIN accepted.")
                return display_maintenance_menu(username, userParameters,blockedTime)
            else:
                print('Incorrect PIN!')
                start = time.time()
                blockedTime = start + 120
        print("\n == You've exceeded the number of tries available and have been locked out for 2 minutes. == \nReturning to the main menu..." )
        
        return userParameters, blockedTime
    
    else:
        print("Too many tries! You have been locked out of the system.")
        print("Time remaining:", int((blockedTime-time.time())//60), 'min' ,round((blockedTime-time.time())%60), 's' )
        return userParameters, blockedTime


def normal_mode(username, userParameters, dataList,dataList2,thermistorList, predeterminedHeight, board):
    """
    Includes the polling loop and displays the distance from nearest vehicle, pedestrian presence and stages of operation.
        Parameters:
            username (key): stores username of profile.
            userParameters (dict): contains a dictionary of stored user profiles.
            dataList (list of integers): list of latest values (distances in cm) polled from the sensor
            dataList2 (list of integers): list of latest values (heights in cm) polled from the sensor
            thermistorList (list of floats): list of latest values (temperatures in degree C) polled from thermistor
            predeterminedHeight (int): height limit of vehicles
            board: communication set-up with arduino
        Returns:
            Function returns updated dataList, dataList2, and thermistorData
    """
    if not userParameters:
        print("\nNo users found.")
        print("Please go to Maintenance Adjustment Mode to set user...")
        return dataList, dataList2, thermistorList
    
    username = list(userParameters.keys())[0] # Get the user from the dictionary
    predeterminedHeight = userParameters[username]["predeterminedHeight"]
    polledData = dataList  # Initialize polledData here
    polledData2 = dataList2

    if slide_switch_on(board, 8):
        print("\nSlide Switch has been turned ON! Exiting to main menu....")
        return polledData, polledData2, thermistorList

    while True:
        try:
            pedestrianPresses = -1
            stage_one(board)
            start = 0 
            start= time.time() 
            end = time.time()
            stageChangedCycle = False
            stageChangedThermistor = False
            stageChangedButton = False
            stageTime = 30
            while end <  start + stageTime: 
                pedestrianPresses, polledData,polledData2,thermistorList, dayNightCycle, slideSwitchIsOn = polling_loop(board, polledData, polledData2, "STG1",pedestrianPresses, predeterminedHeight, thermistorList)
                if slideSwitchIsOn:
                    print('\nSlide Switch has been turned ON! Exiting to main menu....')
                    return polledData, polledData2, thermistorList
                if dayNightCycle == 'night' and stageChangedCycle == False:
                    stageTime = 45
                    stageChangedCycle = True
                if len(thermistorList) >= 1 and thermistorList[-1] > 35 and stageChangedThermistor == False:
                    stageTime += 5
                    stageChangedThermistor = True
                
                if pedestrianPresses > 0 and stageChangedButton == False:
                    if (stageTime - (time.time()-start) ) > 5:
                        stageTime = (time.time()-start) + 5
                        stageChangedButton = True
                print('TOTAL STAGE TIME NOW: ', round(stageTime))
                end = time.time()
                dist_to_nearest_vehicle(int(start-end), polledData)

            stage_two(board)
            start = 0 
            start = time.time()
            stageChangedDist = False
            stageTime = 3
            while end < start + stageTime: 
                pedestrianPresses, polledData,polledData2,thermistorList, dayNightCycle, slideSwitchIsOn = polling_loop(board, polledData, polledData2, "STG2",pedestrianPresses, predeterminedHeight, thermistorList)
                if slideSwitchIsOn:
                    print('\nSlide Switch has been turned ON! Exiting to main menu....')
                    return polledData, polledData2, thermistorList
                if polledData[-1] <= userParameters[username]["distanceRange"] and stageChangedDist == False:
                    print('== EXTENDING YELLOW LIGHT TIME BY 3 SECONDS.......')
                    stageTime += 3
                    stageChangedDist = True
                end = time.time()
                dist_to_nearest_vehicle(int(start-end), polledData)

            stage_three(board)
            start = 0 
            start = time.time()
            while end < start + 3:
                pedestrianPresses, polledData,polledData2,thermistorList, dayNightCycle, slideSwitchIsOn = polling_loop(board, polledData, polledData2, "STG3",pedestrianPresses, predeterminedHeight, thermistorList)
                if slideSwitchIsOn:
                    print('\nSlide Switch has been turned ON! Exiting to main menu....')
                    return polledData, polledData2, thermistorList
                end = time.time()
                dist_to_nearest_vehicle(int(start-end), polledData)

            #stage three with print pedestrian count 
            if pedestrianPresses == -1:
                print('Number of Pedestrain Button Presses:',0)
            else:
                print('Number of Pedestrain Button Presses:',pedestrianPresses)

            stage_four(board)
            start = 0 
            start = time.time()
            stageTime = 30
            stageChangedCycle = False
            stageChangedThermistor = False
            while end < start + stageTime:
                pedestrianPresses, polledData,polledData2,thermistorList, dayNightCycle, slideSwitchIsOn  = polling_loop(board, polledData, polledData2, "STG4",pedestrianPresses, predeterminedHeight, thermistorList)
                if slideSwitchIsOn:
                    print('\nSlide Switch has been turned ON! Exiting to main menu....')
                    return polledData, polledData2, thermistorList
                if dayNightCycle == 'night' and stageChangedCycle == False:
                    stageTime = 10
                    stageChangedCycle = True
                if len(thermistorList) > 1 and thermistorList[-1] > 35 and stageChangedThermistor == False:
                    stageTime += 5
                    stageChangedThermistor = True

                end = time.time()
                dist_to_nearest_vehicle(int(start-end), polledData)

            stage_five(board)
            board.set_pin_mode_digital_output(16)
            board.digital_write(16, 1) #for stage five buzzer
            start = 0 
            start = time.time()
            while end < start + 3:
                pedestrianPresses, polledData,polledData2,thermistorList, dayNightCycle, slideSwitchIsOn  = polling_loop(board, polledData, polledData2, "STG5",pedestrianPresses,predeterminedHeight, thermistorList)
                if slideSwitchIsOn:
                    print('\nSlide Switch has been turned ON! Exiting to main menu....')
                    return polledData, polledData2, thermistorList
                end = time.time()
                dist_to_nearest_vehicle(int(start-end), polledData)
            board.digital_write(16, 0)

            stage_six(board)
            start = 0 
            start = time.time()
            while end < start + 3:
                pedestrianPresses, polledData,polledData2,thermistorList, dayNightCycle, slideSwitchIsOn = polling_loop(board, polledData, polledData2, "STG6",pedestrianPresses, predeterminedHeight, thermistorList)
                if slideSwitchIsOn:
                    print('\nSlide Switch has been turned ON! Exiting to main menu....')
                    return polledData, polledData2, thermistorList
                end = time.time()
                dist_to_nearest_vehicle(int(start-end), polledData)

            
        except KeyboardInterrupt:
            print('\nReturning to main menu...')
            return polledData, polledData2, thermistorList


def polling_loop(board, polledData,polledData2, stage, pedestrianPresses, predeterminedHeight, thermistorList): 
    """
    Polls data from the sensors and checks the pedestrian button for pushes for stages 1-3
        Parameters:
            board: communication set-up with arduino
            polledData (list of integers): list of latest values (distances in cm) polled from the sensor
            polledData2 (list of integers): list of latest values (heights in cm) polled from the sensor
            stage (str): the current stage number
            pedestrianPresses (int): number of presses detected
            predeterminedHeight (int): height limit of vehicles
            thermistorList (list of floats): list of latest values (temperatures in degree C) polled from thermistor  
        Returns:
            Function returns updated pedestrianPresses, polledData, polledData2, thermistorList and the 
            states of the slide switch and day/night cycle from LDR
    """

    start = time.time()
    polledData = ultraSonic(12, 13,board, polledData,stage)
    polledData2 = ultrasonic_height(6,7,board, polledData2, predeterminedHeight)
    thermistorList = thermistor(board, thermistorList)
    cycle = read_LDR(0, board)
    end2 = time.time()
    slideSwitchIsOn = False
    
    if stage in ["STG1", "STG2", "STG3"]:
        while end2 - start < 3:
            pedestrianPresses = ped_presence(2,board,pedestrianPresses) #CHANGE PIN
            slideSwitchIsOn = slide_switch_on(board, 8)
            if slideSwitchIsOn:
                return pedestrianPresses, polledData,polledData2,thermistorList, cycle, slideSwitchIsOn

            time.sleep(0.2)
            end2 = time.time()
    else:
        while time.time() - start < 3:
            slideSwitchIsOn = slide_switch_on(board, 8)
            if slideSwitchIsOn:
                return pedestrianPresses, polledData,polledData2,thermistorList, cycle, slideSwitchIsOn
            time.sleep(0.2)
        #time.sleep(abs(3-(end2-start)))  
    
    end3 = time.time()
    difference2 = end3 - start
    pollingTime = round(difference2, 2)
    print(f'Time Taken: {pollingTime} seconds')
    return pedestrianPresses, polledData,polledData2,thermistorList, cycle, slideSwitchIsOn

def display_maintenance_menu(username, userParameters, blockedTime):
    """
    Displays menu for Maintenace Adjustment Mode menu.
        Parameters:
            username (key): stores username of profile.
            userParameters (dict): contains a dictionary of stored user profiles.
            blockedTime (int): time for which the user is blocked from maintenance mode
        Returns:
            Function returns userParameters and blockedTime.
    """
    start = time.time()

    username = list(userParameters.keys())[0]
    print ("\n=== Maintenence Adjustment Menu ===\n")
    print("1: Change PIN")
    print("2: View/update predetermined vehicle height in cm")
    print("3. View/update vehicle distance to extend main road yellow light in cm")
    print("0: Return to main menu\n")

    selection = -1
    while True:
        try:
            selection = int(input("Option: "))
            if time.time() - start > 60:
                print("Connection Timed Out! Returning to main menu....")
                return userParameters, blockedTime

            if selection in [0, 1, 2, 3]:
                break
            else:
                print("Invalid Option")
        except ValueError:
            print ("Invalid input: only numbers are accepted")
        
    if selection == 1:
        #since this function is already inside authorize_user, we dont need to authorize user again
        newPin = input("Enter new PIN: ")

        if time.time() - start > 60:
            print("Connection Timed Out! Returning to main menu....")
            return userParameters, blockedTime

        print ("PIN changed!")
        userParameters[username]['pin'] = newPin
    elif selection == 2:

        while True:
            print(f"\nCurrent height is {userParameters[username]['predeterminedHeight']} cm")
            newDistance = int(input("Enter new height: "))

            if time.time() - start > 60:
                print("Connection Timed Out! Returning to main menu....")
                return userParameters, blockedTime
            
            if newDistance < 10 or newDistance>23:
                print("Please enter a height between 10-23 cm (inclusive)!")
                pass
            else:
                break
        
        print('Height changed!')
        userParameters[username]['predeterminedHeight'] = newDistance
    elif selection == 3:
        while True:
            print(f"\nCurrent distance is {userParameters[username]['distanceRange']} cm")
            newDistance = int(input("Enter new distance: "))

            if time.time() - start > 60:
                print("Connection Timed Out! Returning to main menu....")
                return userParameters, blockedTime
            
            if newDistance < 10 or newDistance>20:
                print("Please enter a distance between 10-20 cm (inclusive)!")
                pass
            else:
                break
        
        print('Distance changed!')
        userParameters[username]['distanceRange'] = newDistance
    elif selection == 0:
        print('\nBack to main menu...')

    return userParameters, blockedTime

def display_data_observation_menu(polledData, polledData2, thermistorData):
    """
    Displays the Data Observation Mode menu.
        Parameters:
            polledData (list of integers): Conatins the latest data (distances in cm) polled from sensor.
            polledData2 (list of integers): list of latest values (heights in cm) polled from the sensor
            thermistorData (list of floats): list of latest values (temperatures in degree C) polled from thermistor
        Returns:
            Function has no returns
    """

    print("\n=== Data Observation Mode ===\n")
    print("1: Display graph of traffic distance for the last 20 seconds for the last normal operation.")
    print("2: Display graph of vehicle heights for the last 20 seconds for the last normal operation.")
    print("3: Display graph of temperatures for the last 20 seconds for the last normal operation.")
    print("4: Display a message on the seven segment display")
    print("5: Display the average velocity of the vehicles for last 20 secs.")
    print("0. Return to main menu.\n")

    choice = -1 
    # Wait for input
    while True:
        try:
            choice = int(input("Option: "))
            if choice in [0, 1, 2, 3, 4, 5]:
                break
            else:
                print("Error: Invalid option")
        except ValueError:
            print("Error: Only numbers are accepted")

    if choice == 1:
        if len(polledData)<7:
            print('Insuffiecient Data Available!')
        else:
            graphing_distance(polledData)
            print('Graph is displayed')
    elif choice == 2:
        if len(polledData2)<7:
            print('Insuffiecient Data Available!')
        else:
            graphing_height(polledData2)
            print('Graph is displayed')
    elif choice == 3:
        if len(thermistorData)<7:
            print('Insuffiecient Data Available!')
        else:
            graphing_temperature(thermistorData)
            print('Graph is displayed')
    elif choice == 4:
        userinput_sevenseg()
    elif choice == 5:
        if len(polledData) < 7:
            print('Insuffiecient Data Available!')
        else:
            print(f"The average velocity is: {average_velocity(polledData, 21.0)} cm/s")  
    elif choice == 0:
        return
    
def average_velocity(distances, time):
    """
    Displays the Data Observation Mode menu.
        Parameters:
            distances (list of integers): Conatins the latest data (distances in cm) polled from sensor.
            time (float): time in second over which the average velocity is to be calculated
        Returns:
            Function returns average velocity in cm/s (float)
    """
    return round(sum(distances)/time, 3)

def lights(stage,board): 
    """
    Main function which controls the functionality of the LEDs
        Parameters:
            stage (str): Name of stage
            board: communication set-up with arduino
        Returns:
            Function has no return
    """   

    RCLK = 9;  #latchPIN
    SRCLK = 10; #clockPIN
    SER = 8 #data 
    GND = 11; #GNDPin

    if stage == 'stageOne':
        ON = "10000101"[::-1]
    if stage == 'stageTwo':
        ON = "01000101"[::-1]
    if stage == 'stageThree':
        ON = "00100101"[::-1]
    if stage == 'stageFour':
        ON = "00110010"[::-1]
    if stage == 'stageFive':
        ON = "00101010"[::-1]
    if stage == 'stageSix':
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
        if stage == 'stageFive':
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
        elif stage == 'stageFour':
            board.digital_write(GND,1) #initialsing voltage to be ON 
        else:
            board.digital_write(GND,0) #turning it off   

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

def display_current_stage_traffic_operation(stage):
    """
    Displays the current traffic operation stage.
        Parameters:
            stage (String): Name of stage.
        Returns:
            Function has no returns
    """
    print(f"\nThe current stage of traffic is: {stage}")
    
def stage_one(board): 
    """
    Used to control stage one operations for LEDs.
        Parameters:
            board: communication with arduino
        Returns:
            Function has no returns
    """
 
    currentStage = '~~ STAGE ONE ~~'
    display_current_stage_traffic_operation(currentStage)
    lights('stageOne',board)

    #turn on the main road traffic lights --> green
    
    #turn on the side road traffic lights --> red
    
    #turn on the pedestrian lights --> red
    
    print("\nStage one: Main Road Traffic Lights turn green, Side Road Traffic Lights turn red, Pedestrian Lights turn red")
    

def stage_two(board): 
    """
     Used to control stage two operations for LEDs.
        Parameters:
            board: communication with arduino
        Returns:
            Function has no returns
    """
    currentStage = '~~ STAGE TWO ~~'
    display_current_stage_traffic_operation(currentStage)
    lights('stageTwo',board)

    #turn on the main road traffic lights --> yellow

    #turn on the side road traffic lights --> red

    #turn on the pedestrian lights --> red
 
    print("\nStage two: Main Road Traffic Lights turn yellow, Side Road Traffic Lights turn red, Pedestrian Lights turn red")

 
def stage_three(board): 
    """
     Used to control stage three operations for LEDs.
        Parameters:
            board: communication with arduino
        Returns:
            Function has no returns
    """
    currentStage = '~~ STAGE THREE ~~'
    display_current_stage_traffic_operation(currentStage)
    lights('stageThree',board)

    #turn on the main road traffic lights --> red
    
    #turn on the side road traffic lights --> red

    #turn on the pedestrian lights --> red
    
    print("\nStage three: Main Road Traffic Lights turn red, Side Road Traffic Lights turn red, Pedestrian Lights turn red")


def stage_four(board): 
    """
    Used to control stage four operations for LEDs.
        Parameters:
            board: communication with arduino
        Returns:
            Function has no returns
    """
    currentStage = '~~ STAGE FOUR ~~'
    display_current_stage_traffic_operation(currentStage)
    lights('stageFour',board)

    #turn on the main road traffic lights --> red

    #turn on the side road traffic lights --> green

    #turn on the pedestrian lights --> green
    
    print("\nStage four: Main Road Traffic Lights turn red , Side Road Traffic Lights turn green, Pedestrian Lights turn green")


def stage_five(board): 
    """
    Used to control stage five operations for LEDs.
        Parameters:
            board: communication with arduino
        Returns:
            Function has no returns
    """
    currentStage = '~~ STAGE FIVE ~~'
    display_current_stage_traffic_operation(currentStage)
    lights('stageFive',board)

    #turn on the main road traffic lights --> red
    
    #turn on the side road traffic lights --> yellow 
    
    #turn on the pedestrian lights --> flashing green at 2-3 Hz 
    
    print("\nStage five: Main Road Traffic Lights turn red, Side Road Traffic Lights turn yellow, Pedestrian Lights turn flashing green at 2 Hz")  


def stage_six(board): 
    """
    Used to control stage six operations for LEDs.
        Parameters:
            board: communication with arduino
        Returns:
            Function has no returns
    """
    currentStage = '~~ STAGE SIX ~~'
    display_current_stage_traffic_operation(currentStage)
    lights('stageSix',board)

    #turn on the main road traffic lights --> red
    
    #turn on the side road traffic lights --> red
    
    #turn on the pedestrian lights --> red
    
    print("\nStage six: Main Road Traffic Lights turn red, Side Road Traffic Lights turn red, Pedestrian Lights turn red")
    time.sleep(3)

def dist_to_nearest_vehicle(totalTime, sensorDistances):
    """
    Determines distance to nearest vehicle
        Parameters:
            totalTime (float): Contains the time passed in secs from beginning of the stage.
            sensorDistances (list of integers): Conatins the latest data (distances in cm) polled from sensor.
        Returns:
            Function has no returns.
    """
    if round(totalTime) % 3 == 0:
        print(f"The distance to the nearest vehicle is : {sensorDistances[-1]} cm")

def main():
    """
    Main function which runs the program and indicates the starting point.
        Paramters:
            Function has no paramters.
        Returns:
            Function has no returns. 
    """
    userParameters = {} # initialise user parameters dictionary
    username = 'default_user' # prevents unboundlocalerror
    polledData = [] #list which will be updated during normal operation
    polledData2 = []
    predeterminedHeight = 21
    board = pymata4.Pymata4() #set up arduino connection
    blockedTime = 0 #time used for authorization
    thermistorList = []

    while True:
        username, userParameters, polledData, polledData2, thermistorList, predeterminedHeight, blockedTime= display_main_menu(username, userParameters, polledData,polledData2,thermistorList, predeterminedHeight, board, blockedTime)

if __name__ == '__main__':
    main()
