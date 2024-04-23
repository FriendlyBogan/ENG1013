
# Implement polling loop and related placeholders for Milestone 2 part 1
# Created By : Team A12: Nudara, Cooper, Devni, Kristian, Naailah
# Created Date: 01/04/2024
# version ='8.0'

import time
from input_UltraSonic import ultraSonic
from pymata4 import pymata4
from graphing import graphing
from pedpress import pedPresence
#board = pymata4.Pymata4()
proceedData = []
# Define trigger and echo pins
triggerPin = 2
echoPin = 3
#board.set_pin_mode_sonar(triggerPin, echoPin, timeout=20000)

# Global starting point 
authorization = 'Allowed'
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

SOME NOTES FOR NEXT MEETING: (Naailah)
- what is the "Distance" parameter that we are allowing the user to change (see maintenance adjustment)? This is there all over the file with the name distanceCm
- See how to integrate ultrasonic sensor function and normal_mode() since they both have loops. Also make the distance to nearest vehicle work.
- ENSURE traffic_operation_sequence(totalTime, sensor_distance) IS NOT DISRUPTED in the process of integrating the sensors
- for the distance_to_nearest_vehicle, validate the data, if no data available, print relevant message
- ped_presence (check spelling) should be imported from the input_pedPresence file? how to integrate in the normal mode? Ensure the number of presses displayed at stage 3
- delete the get_sensor_data function (repetitive, no longer necesary?)
- See if peak_traffic_time() is working, if not, better to remove it
- average_velocity() why are there two of them?
- See how graphs are going and how the data can be accessed for the graphs
- display_current_stage_traffic_operation(stage) function is unecessary, we can directly print it under the stage functions (use the same ofrmat tho, it looks neat)
- How to use call-back functions.
- change pin to user_pin since can be confused with arduino pins
- Global variables have been initialized twice, change that !!(changed in the branch)!!
- Get atleast the normal mode working properly with LEDs
- check with the branched polling loop which i made some changes to

FROM BRIEF:
- Probe points for current measurement? Use jumper pins not wires (there are guides on moodle)
- see that there are appropriate print statements
- The time between polling cycles (time between each cycle of ‘sensor polling’) is between 1 and 5 seconds, Have we included this?
- DONT FORGET CIRCUIT DIAGRAMS FOR SUBMISSION!!
- Record working circuit video
- Finally, remove extra things from the coding files and check coding standards
- chcek graphs are appropriately formatted

QUESTIONS/QUERIES (Nudara):
- line 100 - does it work when there is a While sonar read is true? Because the sonar read doesn't give boolean? (also why is it in a function header format with the triple quotations)
- line 110 - why is finalTime assigned as a variable if it is not used in the function? In line 115, another time.time is in substractione eqn
- in the input_polling function, the correct notation should be square brackets for indexing a list not round brackets 
- in line 110 - the code doesn't really check the stability for 3 seconds as we don't have a condition that states if time is 3 seconds & the final item in polledData is the same as the previous item then make it final distance. 
(it is only specified in the comment) 
- if finalDistance is a formal parameter of velocity function we need an argument when the velocity function is called
- I understand that finalTime is a required parameter to the velocity function but it was defined within the input_polling function and hence is only available in the local space. 
- In the display_main_menu function: is the distanceCm a parameter because in this function, the normal mode function is called and it has a parameteer distanceCm?
- Likewise, the authorize_user function and display_data_observation_menu function are called with distanceCm and distanceCm & pin as the parameters respectively(but is it required)?
- In the display_main_menu function: Why are there return statements within the conditional statements?? 
- Is authorize_user function called with an argument for pin as the correct pin (why is distanceCm a parameter for this function - when it is not even used) & why does the function's return values(pin & distance) assigned to newPin, newDistance? 
- polled_data is intialised in the normal_mode function but also at the very top of the code so??? (are both necessary?)
- In normal_mode function for the line: polledData.append(get_sensor_data()) --> get_sensor_data is a print statement & it has no returns so why is it getting added to polledData (a list)?? --> the only thing added to that list will be 'None'. 
- There is a display_maintenance_menu function but it is never called anywhere ! Only the authorize_user function is displayed? 
- Polled_data is ALSO initialised in the main function (towards the bottom) ?? 

"""
"""
Some Answers to questions above (Cooper)
Input functions:
1."what is the "Distance" parameter that we are allowing the user to change (see maintenance adjustment)? This is there all over the file with the name distanceCm"
- for this i will add a function within my loop to use the user defined parameters as the maximum distance detection(i dont know the actual parameter we're changing)
so this will do for now as the user defined parameter. 
2. See how to integrate ultrasonic sensor function and normal_mode() since they both have loops. Also make the distance to nearest vehicle work.
- The integration i had a couple ideas, that is inplementing the input within the normmal loop like you said, but have a condition that triggers the input loop to run. 
- the distance to nearest vehicle can be done just by implementing a code in the output function that calls for the distancedata within the input loop then it would be fine
3. - ped_presence (check spelling) should be imported from the input_pedPresence file? how to integrate in the normal mode? Ensure the number of presses displayed at stage 3
- the input_pedPresense IS the working one. but i overlooked that this needs to be runned at all times with the loop. so i changed it to just a file and we can put that somewhere in the control loop
4. The time between polling cycles (time between each cycle of ‘sensor polling’) is between 1 and 5 seconds, Have we included this?
- i completely overlooked this. I changed the input_Ultrasonic into a 5 seconds loop. 
5. - average_velocity() why are there two of them? 
- all the old input functions are not working. so do not worry about it. only look at input_xxx for the working file
6. Nudara's questions, all the input functions in  this file does not work. Look at the other files labeled input_xxx for the new working files.

Questions
1. How are we doing the pooling loop for hte normal mode? like maybe a input loop within the normal mode and the LEDs run indepedantly? 
2. Arduino pin allocations, might need to split people up into groups for the meeting. some do the circuit some do the programming. 

QUESTIONS -Devni
-Do we not store the data in pairs (eg: distance, timestamp)?
"""

def display_main_menu(pin, distanceCm,polledData, board):
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
        polledData = normal_mode(distanceCm,polledData, board)
        return pin, distanceCm, polledData
    elif choice == 2:
        newPin, newDistance = authorize_user(pin, distanceCm)
        if newPin is not None:
            return newPin, newDistance,polledData
        else:
            return pin, distanceCm, polledData
    elif choice == 3:
        display_data_observation_menu(polledData)
        return pin, distanceCm, polledData
    elif choice == 0:
        print("Shutting the system down...")
        quit()

def authorize_user(pin, distanceCm):
    """
    Used to authorize user to access the Maintenance Adjustment settings
        Parameters:
            pin (str): PIN for authorization
            distanceCm (str): distance in cm
        Returns:
            Function returns pin and distanceCm, which can be changed by user inputs
    """
    #ask for PIN, 5 times max, then return to main menu (Lock person out of system settings) (for maintenace adjustment mode)
    for tries in range(5):
        userPin = input('\nEnter PIN: ')
        if userPin == pin:
            print('PIN accepted.')
            return display_maintenance_menu(pin, distanceCm)
        else:
            print('Incorrect PIN!')
    print("You've exceeded the number of tries available and have been locked out. Returning to the main menu..." )
    return pin, distanceCm

1
def normal_mode(distanceCm,data_list, board):
    """
    Includes the polling loop and displays the distance from nearest vehicle, pedestrian presence and stages of operation.
        Parameters:
            distanceCm (str): used to print the distance between vehicles
        Returns:
            Function has no returns
    """
    totalTime = 0
    polledData = data_list  # Initialize polledData here (check notes)
    
 
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
                polling_loop(board, polledData, 'one', pedestrianPresses)
                end = time.time()
                dist_to_nearest_vehicle(int(start-end), polledData)

            stage_two()
            #stage two lights etc. 
            start = 0 
            start = time.time()
            while end < start + 3: 
                pedestrianPresses = polling_loop(board, polledData, 'two',pedestrianPresses)
                end = time.time()
                dist_to_nearest_vehicle(int(start-end), polledData)

            stage_three()
            start = 0 
            start = time.time()
            while end < start + 3:
                pedestrianPresses = polling_loop(board, polledData, 'three', pedestrianPresses)
                end = time.time()
                dist_to_nearest_vehicle(int(start-end), polledData)
            #stage three with print pedestrian count 
            print('Number of Pedestrain Button Presses:',pedestrianPresses-1)

            stage_four()
            start = 0 
            start = time.time()
            while end < start + 30:
                polling_loop(board, polledData, 'four',pedestrianPresses)
                end = time.time()
                dist_to_nearest_vehicle(int(start-end), polledData)

            stage_five()
            start = 0 
            start = time.time()
            while end < start + 3:
                polling_loop(board, polledData, 'five',pedestrianPresses)
                end = time.time()
                dist_to_nearest_vehicle(int(start-end), polledData)

            stage_six()
            start = 0 
            start = time.time()
            while end < start + 3:
                polling_loop(board, polledData, 'six',pedestrianPresses)
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
    return pedestrianPresses

def display_maintenance_menu(pin, distanceCm):
    """
    Displays menu for Maintenace Adjustment Mode.
        Parameters:
            pin (str): for storing the values of the new pin
            distanceCm (str): for storing the values of the new distance
        Returns:
            Function returns pin and distanceCm for storage and updated value purposes
    """
    #function should show user what parameters can be changed (PIN and the distance - globals )
    print ("\n=== Maintenence Adjustment Menu ===\n")
    print("1: Change PIN")
    print("2: View/update distance (range) in cm")
    print("0: Return to main menu\n")

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
        newPin = input ("Enter new PIN: ")
        print (f"PIN changed!")
        return newPin, distanceCm
     
    elif selection == 2:
        print(f"Current distance is {distanceCm} cm")
        newDistance = int(input("Enter new distance: "))
        print('Distance changed!')
        return pin, newDistance
    elif selection == 0:
        return pin, distanceCm

def display_data_observation_menu(polledData):
    """
    Displays the Data Observation menu.
        Parameters:
            polledData (list): Conatins the data polled from sensors.
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
            if choice == 1 or choice == 2 or choice == 3 or choice==0:
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
            print('Graph is printed')
    elif choice == 2:
        print('Please run the seven segment file to do so!')
    elif choice == 3:
        if len(polledData) < 7:
            print('Insuffiecient Data Available!')
        else:
            print(f"The average velocity is: {average_velocity(polledData, 21)}")  
    elif choice == 0:
        return
    
def average_velocity(distances, time):
    return round(sum(distances)/time, 3)

#Output Subsytem begins here 
#function to display the current stage of traffic operation occuring to console 
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
    pin = '1234' # set default pin
    distanceCm = 0 # set default distance
    polledData = []  #is this needed? RESETS FOR EVERY NORMAL OPERATRION RUN
    board = pymata4.Pymata4()

    while True:
        pin, distanceCm, polledData= display_main_menu(pin, distanceCm,polledData,board)

if __name__ == '__main__':
    main()
