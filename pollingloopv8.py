
# Implement polling loop and related placeholders for Milestone 2 part 1
# Created By : Team A12: Nudara, Cooper, Devni, Kristian, Naailah
# Created Date: 01/04/2024
# version ='8.0'

import time
#from pymata4 import pymata4
#board = pymata4.Pymata4()
proceedData = []
# Define trigger and echo pins
triggerPin = 2
echoPin = 3
#board.set_pin_mode_sonar(triggerPin, echoPin, timeout=20000)

# Global starting point 
distanceCm = 0 # will need to change when setting up the aparatus
polledData = [] # will be updated under normal operation
PIN = '1234' #can be changed under maintenance adjustment
authorization = 'Allowed'
#some other parameters which the user can modify under the maintenance adjustment
pedestrianPresses = 0 #set the following to zero as input subsystem not included in this code
distance = 0

def pedPresense():
    """
    Used to detect presence of pedestrians (placeholder)
        Parameters:
            Function has no parameters
        Returns:
            pedestrianPresses (int) : Number of presses

    """
    global pedestrianPresses
    pedStarting = time.time()
    '''
    if board.digital.read(5) == 1:#check if there is a signal from the pin, if there is press +1 
        pedestrianPresses += 1
    return pedestrianPresses
    '''

def input_polling():
    """
    Used to control ineraction with arduino (not yet used)
        Parameters:
            Function has no parameters
        Returns:
            timeinLoop in seconds and proceedData after the filtering process 
    """

    # start by defining the starting time for the function, input the function to the pin,
    # pin will read the information on the pin then the data gets send back to arduino
    print('start input polling')
    # collect measurements while checking keyboard interrupts
    """
    while True:
        try:
            # Measuring at 1 Hz frequency
            pollingStarting = time.time() #defining the starting time for the function 

            '''
            while board.sonar_read(triggerPin) is True :  #collect data if the sensor is activated 
                polledData.append(board.sonar_read(triggerPin))
                time.sleep(1)
            '''

            initialDistance = polledData(0) #set the first distance detected as the inital distance 

            if polledData(-1) == polledData(+1): #if the data is stationary for 3 seconds then store the distance as final distance
                finalDistance = polledData(-1)
                finalTime = time.time()
            
            for data_point in polledData: #data processing to check if all data points are within the range
                if abs(data_point - initialDistance) <= 50:  
                    proceedData.append(round(data_point,2))
            timeInLoop = time.time() - pollingStarting

            return timeInLoop 
            return proceedData 
        except KeyboardInterrupt:
            exit()
        """



def velocity():
    """ 
    Calculate the velocity from the measured distances in the input function and the time measured in the input function
        Parameters:
            Function has no parameters
        Returns:
            Returns a variable named AvgVel in m/s  

    """
    #avgVel = (finalDistance/100)-(initalDistance/100)/finalTime #calculate the avgvel in m/s 
    #if avgVel > 30: #checks for any speeding vehicle, but needs to be tweaked with experiments
        #speedingVel = avgVel
        #return speedingVel
    #else:
        #return avgVel 



def display_main_menu():
    """
    Used to display the main menu.
        Parameters:
            Function has no parameters
        Returns:
            Function has no returns

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
            if choice == 1 or choice == 2 or choice == 3 or choice==0:
                break
            else:
                print("Error: Invalid option")
        except ValueError:
            print("Error: Only numbers are accepted")

    # Process choice
    if choice == 1:
        normal_mode()
    elif choice == 2:
        authorize_user(PIN)
    elif choice == 3:
        display_data_observation_menu(polledData)
    elif choice == 0:
        print("Shutting the system down...")
        quit()

def authorize_user(pin):
    """
    Used to authorize user to access the Maintenance Adjustment settings
        Parameters:
            Function has no parameters
        Returns:
            Function has no returns
    """
    #ask for PIN, 5 times max, then return to main menu (Lock person out of system settings) (for maintenace adjustment mode)
    global authorization

    if authorization == 'Allowed':
        for tries in range(5):
            userPin = input('\nEnter PIN: ')

            if userPin != pin:
                print('Incorrect PIN!')
            else:
                display_maintenance_menu()
                return
            
    authorization = 'Not Allowed'
    print("You've exceeded the number of tries available and have been locked out. Returning to the main menu...")

def normal_mode():
    """
    Includes the polling loop and displays the distance from nearest vehicle, pedestrian presence and stages of operation.
        Parameters:
            Function has no parameters
        Returns:
            Function has no returns
    """
    totalTime = 0

    while True:
        try:
            start = time.time()
            get_sensor_data()
            current = time.time()

            time.sleep(1)
            end = time.time()
            pollingTime = round(end-start, 4)
            print(f'Time Taken: {pollingTime} seconds')

            totalTime += (pollingTime)
            #run the output traffic operation sequence 
            result = traffic_operation_sequence(totalTime)

            if result == 'Last Stage reached':
                totalTime = 0

            
        except KeyboardInterrupt:
            print('\nReturning to main menu...')
            return
    

def get_sensor_data():
    """
    Placeholder function used to get data from sensors.
        Parameters:
            Function has no parameters
        Returns:
            Function has no returns
    """
    print('Data is obtained from ultrasonic sensors and added to polledData')

def display_maintenance_menu():
    """
    Displays menu for Maintenace Adjustment Mode.
        Parameters:
            Function has no parameters
        Returns:
            Function has no returns
    """
    #function should show user what parameters can be changed (PIN and the distance - globals )
    print ("\n=== Maintainence Adjustment Menu ===\n")
    print("1: Change PIN")
    print("2: View/update distance (range) in cm")
    print("0: Return to main menu\n")

    global PIN
    global distanceCm
    while True:
        try:
            selection = int(input("Option: "))
            if selection == 1 or selection == 2 or selection == 0:
                break
            else:
                print("Invalid Option")
        except ValueError:
            print ("Invalid input: only numbers are accepted")
        
    if selection == 1:
        #since this function is already inside authorize_user, we dont need to authorize user again
        newPin = input ("Enter new PIN: ")
        PIN = newPin
        print (f"PIN changed!")
    elif selection == 2:
        print(f"Current distance is {distanceCm} cm")
        newDistance = int(input("Enter new distance: "))
        distanceCm = newDistance
        print("Distance changed!")
    elif selection == 0:
        return


def peak_traffic_time(polledData):
    """
    Used to detect the peak traffic time for past 24 hours. (yet to be implemented)
        Parameters:
            polledData (list): Conatins the data polled from sensors
        Returns:
            Function has no returns
    """

    #get past 24 times, put times in a dictionary and count the number at each time, highest = peak
    verifyTwentyFourHoursAgo = time.time() - (3600 * 24)
    #put it in a for loop to go through each polled data to see if its in the past 24h
    twentyFourHoursTimestamps = []
    for timestamps in polledData:
        if timestamps >= verifyTwentyFourHoursAgo:
            twentyFourHoursTimestamps.append(timestamps)
    if twentyFourHoursTimestamps:
        hour_count = {}
        for hourTimestamps in twentyFourHoursTimestamps:
            hours = time.localtime(hourTimestamps).tm_hour
            hour_count[hour] + 1
    
        peak_times = []
        max = 0
        for hour, count in hour_count.items():
            if count > max:
                peak_times = count
                max = count
            elif count == max:
                peak_times.append(count)
            else:
                pass
        print (f"The peak traffic time(s) was {peak_times}")
    else:
        print("Insufficient data available!")

def average_velocity():
    """
    Used to calculate average velocity of vehicles.
        Parameters:
            Function has no parameters
        Returns:
            averageVelocity (float): The calculated average value
    """
    data = '?'
    totalVelocity = sum #(whats the data?)
    averageVelocity = '?'
    #averageVelocity = totalVelocity / len(totalVelocity)
    return averageVelocity

def display_data_observation_menu(polledData):
    """
    Displays the Data Observation menu.
        Parameters:
            polledData (list): Conatins the data polled from sensors.
        Returns:
            Function has no returns
    """

    print("\n=== Data Observation Mode ===\n")
    print("1: Display graph of traffic distance for the last 20 seconds.")
    print("2: Display the peak traffic time in the past 24 hours")
    print("3: Display the average velocity of the vehicles")
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
        if polledData == []:
            print('Insuffiecient Data Available!')
        else:
            print('Graph is printed')
    elif choice == 2:
        peak_traffic_time(polledData)
    elif choice == 3:
        average_velocity()
        print(f"The average velocity is: {average_velocity}")
    elif choice == 0:
        return

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

    global pedestrianPresses
    currentStage = 'Stage one'
    display_current_stage_traffic_operation(currentStage)
    #turn on the main road traffic lights --> green
    
    #turn on the side road traffic lights --> red
    
    #turn on the pedestrian lights --> red
    
    print("\nStage one: Main Road Traffic Lights turn green, Side Road Traffic Lights turn red, Pedestrian Lights turn red")
    pedestrianPresses = 0 #reset pedestrian presses value to zero in stage one 

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
    global pedestrianPresses
    currentStage = 'Stage three'
    display_current_stage_traffic_operation(currentStage)
    #turn on the main road traffic lights --> red
    
    #turn on the side road traffic lights --> red

    #turn on the pedestrian lights --> red
    
    print("\nStage three: Main Road Traffic Lights turn red, Side Road Traffic Lights turn red, Pedestrian Lights turn red")
    print(f"The number of pedestrian presses is : {pedestrianPresses}") #number of pedestrian presses displayed to console during stage three


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

def display_distance_to_nearest_vehicle(polledData):
    """
    Function to display the distance to the nearest vehicle in cm.
        Parameters:
            polledData (list): Conatins the data polled from sensors.
        Returns:
            Function has no returns
    """
    print(f"The distance to the nearest vehicle is : {distance:.2f} cm") #or should I use round function: round(,2)??


def traffic_operation_sequence(totalTime):
    """
    Main function to control the sequence of traffic light operation according to time.
        Parameters:
            totalTime (float): Contains the time passed in secs from beginning of stage one.
        Returns:
            returns the string 'Last Stage reached' when stage six gets over.
    """
    
    if round(totalTime) % 3 == 0:
        display_distance_to_nearest_vehicle(distance)
        # print('The system displays the distance to the nearest vehicle in two decimal cm readings')
  
    if round(totalTime) == 1:
        stage_one()
    elif round(totalTime) == 31:
        stage_two()
    elif round(totalTime) == 33:
        stage_three()
    elif round(totalTime) == 36:
        stage_four()
    elif round(totalTime) == 96:
        stage_five()
    elif round(totalTime) == 99:
        stage_six()
        return 'Last Stage reached'

def main():
    while True:
        display_main_menu()

if __name__ == '__main__':
    main()