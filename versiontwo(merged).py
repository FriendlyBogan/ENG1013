
# Implement polling loop and related placeholders for Milestone 2 part 1
# Created By : Team A12: Nudara, Cooper, Devni, Kristian, Naailah
# Created Date: 01/04/2024
# version ='12.0'

import time
from input_UltraSonic import ultraSonic
from pymata4 import pymata4
from graphing import graphing
from pedpress import pedPresence
from sevensegfinal import start_seven_seg
#board = pymata4.Pymata4()
proceedData = []
# Define trigger and echo pins
triggerPin = 2
echoPin = 3
#board.set_pin_mode_sonar(triggerPin, echoPin, timeout=20000)

# Global starting point 

#some other parameters which the user can modify under the maintenance adjustment
pedestrianPresses = 0 #set the following to zero as input subsystem not included in this code
distance = 0

"""

MAIN THINGS THAT I CHANGED:
- ped_presence() now takes 'pedestrianPresses' as a paramter instead of being accessed globally.
- input_poling() and display_data_observation() accept data as paramters now.
- functions now have return values, such as input_polling() now returns both 'timeInLoop' and 'processData'.
- authorize_user() now passes as 'authorization' as a paramter and returns the modified value.
- display_maintenance_menu() initialises 'PIN' and 'distanceCm' with default values to avoid errors for later accessing in the function.
"""


def display_main_menu(userName, userParameters, polledData, board, authorization):
    """
    Used to display the main menu.
        Parameters:
            pin (str): used for storing pin
            distanceCm (str): used for storing distance
        Returns:
            Function returns pin, distanceCm, newPin, newDistance which indicates the stored data from maintenance mode.

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
        polledData = normal_mode(userName, userParameters, polledData, board)
    elif choice == 2:
        userParameters, authorization = authorize_user(userName, userParameters, authorization)
    elif choice == 3:
        display_data_observation_menu(polledData, board)
    elif choice == 0:
        print("Shutting the system down...")
        board.shutdown()
        quit()

    return userName, userParameters, polledData, authorization

def authorize_user(userName, userParameters, authorization):
    '''
    Used to authorize user to access the Maintenance Adjustment settings
        Parameters:
            userName (key): stores userName of profile.
            userParameters (dict): contains a dictionary of stored user profiles.
        Returns:
            Function returns userParameters
    '''

    if authorization == 'Allowed':
        while True:
            try:
                decision = input("\nDo you want to create a new user profile? (Y/N): ")
                decision = decision.upper() # so if the user inputs Y or y, either way the input is accepted
                if decision == 'Y':
                    userName = input("\nEnter your userName: ")
                    if userName not in userParameters:
                        print("\nCreating new user profile...")
                        pin = input("Set your PIN: ")
                        userParameters[userName] = {
                            'pin': pin,
                            'distanceCm': 0
                        }
                        print("Profile created successfully!")
                    else:
                        print('Username already exists!')
                    return userParameters, authorization
                elif decision == 'N':
                    subsequentProfile = input("Do you already have a profile (Y/N)? ")
                    subsequentProfile = subsequentProfile.upper() # so if the user inputs Y/y, N/n - either way the input is accepted
                    if subsequentProfile == 'Y':
                        userName = input("\nEnter your userName: ")
                        if userName not in userParameters:
                            print("Error. User not found")
                            time.sleep(1)
                        else:
                            break
                    elif subsequentProfile == 'N':
                        print("\nGoing back to main menu...")
                        time.sleep(1)
                        return userParameters, authorization
                    elif decision != 'Y' or 'N':
                        print("Please enter Y or N.")
                elif decision != 'Y' or 'N':
                    print("Please enter Y or N.")
            except KeyboardInterrupt:
                print("\nGoing back to main menu...") # handling for wanting to go back to main menu anywhere in the loop
                time.sleep(1)
                return userParameters, authorization

        #ask for PIN, 5 times max, then return to main menu (Lock person out of system settings) (for maintenace adjustment mode)
        for tries in range(5):
            userPin = input('\nEnter PIN: ')
            if userPin == userParameters[userName]['pin']:
                print("PIN accepted.")
                return display_maintenance_menu(userName, userParameters, authorization)
            else:
                print('Incorrect PIN!')
        print("\n == You've exceeded the number of tries available and have been locked out == \nReturning to the main menu..." )
        authorization = 'Not Allowed'
        return userParameters, authorization
    
    else:
        print("Too many tries! You have been locked out of the system.")
        return userParameters, authorization


def normal_mode(userName, userParameters, dataList, board):
    """
    Includes the polling loop and displays the distance from nearest vehicle, pedestrian presence and stages of operation.
        Parameters:
            userName (key): stores userName of profile.
            userParameters (dict): contains a dictionary of stored user profiles.
        Returns:
            Function has no returns
    """
    if not userParameters:
        print("\nNo users found.")
        print("Please go to Maintenance Adjustment Mode to set user...")
        time.sleep(2) # creates user readability when print statements show.
        return dataList
    
    userName = list(userParameters.keys())[0] # Get the user from the dictionary

    polledData = dataList  # Initialize polledData here (check notes)
    
 
    board.set_pin_mode_sonar(2,3,timeout=150000)
    while True:
        try:
            pedestrianPresses = 0
            stage_one()
           
            start = 0 
            #stage one takes split seconds (must fully run before printing otherwise display insufficient data)
            start= time.time() 
            end = time.time()
            while end <  start +30: 
                # pedestrianPresses = polling_loop(board, polledData, 'one', pedestrianPresses)
                pedestrianPresses, polledData = polling_loop(board, polledData, 'one', pedestrianPresses)
                end = time.time()
                dist_to_nearest_vehicle(int(start-end), polledData)

            stage_two()
            #stage two lights etc. 
            start = 0 
            start = time.time()
            while end < start + 3: 
                pedestrianPresses, polledData = polling_loop(board, polledData, 'two',pedestrianPresses)
                end = time.time()
                dist_to_nearest_vehicle(int(start-end), polledData)

            stage_three()
            start = 0 
            start = time.time()
            while end < start + 3:
                pedestrianPresses, polledData  = polling_loop(board, polledData, 'three', pedestrianPresses)
                end = time.time()
                dist_to_nearest_vehicle(int(start-end), polledData)
            #stage three with print pedestrian count 
            print('Number of Pedestrain Button Presses:',pedestrianPresses-1)

            stage_four()
            start = 0 
            start = time.time()
            while end < start + 30:
                pedestrianPresses, polledData  = polling_loop(board, polledData, 'four',pedestrianPresses)
                end = time.time()
                dist_to_nearest_vehicle(int(start-end), polledData)

            stage_five()
            start = 0 
            start = time.time()
            while end < start + 3:
                pedestrianPresses, polledData  = polling_loop(board, polledData, 'five',pedestrianPresses)
                end = time.time()
                dist_to_nearest_vehicle(int(start-end), polledData)

            stage_six()
            start = 0 
            start = time.time()
            while end < start + 3:
                pedestrianPresses, polledData  = polling_loop(board, polledData, 'six',pedestrianPresses)
                end = time.time()
                dist_to_nearest_vehicle(int(start-end), polledData)

            
        except KeyboardInterrupt:
            print('\nReturning to main menu...')
            return polledData


def polling_loop(board, polledData, stage, pedestrianPresses): 
    start = time.time()
    polledData = ultraSonic(2, 3,board, polledData)
    end = time.time()
    difference = end-start
    end2 = time.time()
    
    if stage in ['one', 'two', 'three']:
        while end2 - start < 3:
            #pedestrianPresses = check_button(8, board, pedestrianPresses, add_pedcount)
            pedestrianPresses = pedPresence(8,board,pedestrianPresses)
            time.sleep(0.2)
            end2 = time.time()
    else:
        time.sleep(abs(3-(difference))) #1 or 1.5 are other possible time lengths 
    
    end3 = time.time()
    difference2 = end3 - start
    pollingTime = round(difference2, 2)
    print(f'Time Taken: {pollingTime} seconds')
    return pedestrianPresses, polledData

def display_maintenance_menu(userName, userParameters, authorization):
    """
    Displays menu for Maintenace Adjustment Mode.
        Parameters:
            userName (key): stores userName of profile.
            userParameters (dict): contains a dictionary of stored user profiles.
        Returns:
            Function returns userParameters
    """
    #function should show user what parameters can be changed (PIN and the distance - globals )
    userName = list(userParameters.keys())[0]
    print ("\n=== Maintenence Adjustment Menu ===\n")
    print("1: Change PIN")
    print("2: View/update distance (range) in cm")
    print("0: Return to main menu\n")

    selection = -1
    while True:
        try:
            selection = int(input("Option: "))
            if selection in [0, 1, 2]:
                break
            else:
                print("Invalid Option")
        except ValueError:
            print ("Invalid input: only numbers are accepted")
        
    if selection == 1:
        #since this function is already inside authorize_user, we dont need to authorize user again
        newPin = input("Enter new PIN: ")
        print ("PIN changed!")
        userParameters[userName]['pin'] = newPin
    elif selection == 2:
        print(f"Current distance is {userParameters[userName]['distanceCm']} cm")
        newDistance = int(input("Enter new distance: "))
        print('Distance changed!')
        userParameters[userName]['distanceCm'] = newDistance
    elif selection == 0:
        print('\nBack to main menu...')

    return userParameters, authorization

def display_data_observation_menu(polledData, board):
    """
    Displays the Data Observation menu.
        Parameters:
            polledData (list): Conatins the data polled from sensors.
            userName (key): stores userName of profile.
            userParameters (dict): contains a dictionary of stored user profiles.
        Returns:
            Function has no returns
    """

    print("\n=== Data Observation Mode ===\n")
    print("1: Display graph of traffic distance for the last 20 seconds for the last normal operation.")
    print("2: Display a message on the seven segment display")
    print("3: Display the average velocity of the vehicles for last 20 secs.")
    print("0. Return to main menu.\n")

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

    if choice == 1:
        if len(polledData)<7:
            print('Insuffiecient Data Available!')
        else:
            graphing(polledData)
            print('Graph is displayed')
    elif choice == 2:
        start_seven_seg()
    elif choice == 3:
        if len(polledData) < 7:
            print('Insuffiecient Data Available!')
        else:
            print(f"The average velocity is: {average_velocity(polledData, 21)} cm/s")  
    elif choice == 0:
        return
    
def average_velocity(distances, time):
    return round(sum(distances)/time, 3)

#Output Subsytem begins here 
#function to display the current stage of traffic operation occuring to console 

def lights(stage):    
    from pymata4 import pymata4
    import time
    board = pymata4.Pymata4()
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
    
def stage_one(): 
    """
    Used to control stage one, resets pedestrianPresses to 0.
        Parameters:
            Function has no parameters
        Returns:
            Function has no returns
    """

 
    currentStage = 'Stage one'
    display_current_stage_traffic_operation(currentStage)
    #turn on the main road traffic lights --> green
    
    #turn on the side road traffic lights --> red
    
    #turn on the pedestrian lights --> red
    
    print("\nStage one: Main Road Traffic Lights turn green, Side Road Traffic Lights turn red, Pedestrian Lights turn red")
    

def stage_two(): 
    """
    Used to control stage two.
        Parameters:
            Function has no parameters
        Returns:
            Function has no returns
    """
    currentStage = 'Stage two'
    display_current_stage_traffic_operation(currentStage)
    #turn on the main road traffic lights --> yellow

    #turn on the side road traffic lights --> red

    #turn on the pedestrian lights --> red
 
    print("\nStage two: Main Road Traffic Lights turn yellow, Side Road Traffic Lights turn red, Pedestrian Lights turn red")

 
def stage_three(): 
    """
    Used to control stage three and display the number of push button presses detected from stage 1.
        Parameters:
            Function has no parameters
        Returns:
            Function has no returns
    """
    currentStage = 'Stage three'
    display_current_stage_traffic_operation(currentStage)
    #turn on the main road traffic lights --> red
    
    #turn on the side road traffic lights --> red

    #turn on the pedestrian lights --> red
    
    print("\nStage three: Main Road Traffic Lights turn red, Side Road Traffic Lights turn red, Pedestrian Lights turn red")


def stage_four(): 
    """
    Used to control stage four.
        Parameters:
            Function has no parameters
        Returns:
            Function has no returns
    """
    currentStage = 'Stage four'
    display_current_stage_traffic_operation(currentStage)
    #turn on the main road traffic lights --> red

    #turn on the side road traffic lights --> green

    #turn on the pedestrian lights --> green
    
    print("\nStage four: Main Road Traffic Lights turn red , Side Road Traffic Lights turn green, Pedestrian Lights turn green")


def stage_five(): 
    """
    Used to control stage five.
        Parameters:
            Function has no parameters
        Returns:
            Function has no returns
    """
    currentStage = 'Stage five'
    display_current_stage_traffic_operation(currentStage)
    #turn on the main road traffic lights --> red
    
    #turn on the side road traffic lights --> yellow 
    
    #turn on the pedestrian lights --> flashing green at 2-3 Hz 
    
    print("\nStage five: Main Road Traffic Lights turn red, Side Road Traffic Lights turn yellow, Pedestrian Lights turn flashing green at 2-3 Hz")  


def stage_six(): 
    """
    Used to control stage six.
        Parameters:
            Function has no parameters
        Returns:
            Function has no returns
    """
    currentStage = 'Stage six'
    display_current_stage_traffic_operation(currentStage)
    #turn on the main road traffic lights --> red
    
    #turn on the side road traffic lights --> red
    
    #turn on the pedestrian lights --> red
    
    print("\nStage six: Main Road Traffic Lights turn red, Side Road Traffic Lights turn red, Pedestrian Lights turn red")
    time.sleep(3)

def dist_to_nearest_vehicle(totalTime, sensorDistances):
    """
    Main function to control the sequence of traffic light operation according to time.
        Parameters:
            totalTime (float): Contains the time passed in secs from beginning of stage one.
        Returns:
            returns the string 'Last Stage reached' when stage six gets over.
    """
    if round(totalTime) % 3 == 0:
        print(f"The distance to the nearest vehicle is : {min(sensorDistances[-1:-4:-1])} cm")

def main():
    """
    Main function which runs the program and controls the timings between inputted data
        Paramters:
            Function has no paramters.
        Returns:
            Function has no returns. 
    """
    userParameters = {} # initialise user paramters dictionary
    userName = 'default_user' # prevents unboundlocalerror
    polledData = []  #is this needed? RESETS FOR EVERY NORMAL OPERATRION RUN
    authorization = 'Allowed'
    board = pymata4.Pymata4()

    while True:
        userName, userParameters, polledData, authorization = display_main_menu(userName, userParameters, polledData, board, authorization)

if __name__ == '__main__':
    main()
