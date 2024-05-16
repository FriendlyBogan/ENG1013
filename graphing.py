# Function to create graph from sensor data
# Created By : Team A12: Nudara, Cooper, Devni, Kristian, Naailah
# Created Date: 20/04/2024
# version: 5.0

import matplotlib.pyplot as plt

def graphing_distance(polledData):
    '''
    Function to create graph from sensor data
        Parameters:
            polledData (list of integers): list of latest values (distances in cm) polled from the sensor
        Returns:
            Function has no returns
    '''

    last20SecTimes=[]
    for i in range(1,22,3):
        last20SecTimes.append(i)

    plt.plot(last20SecTimes, polledData)

    plt.xlabel('Timestamps (s)')
    plt.ylabel('Distances (cm)')
    plt.legend(['Distance']) 
    plt.title("Polled distances from the last 20 seconds vs Time")
    plt.savefig('distance_time_graph.png')
    plt.show()

def graphing_height(polledData2):
    '''
    Function to create graph from sensor data
        Parameters:
            polledData (list of integers): list of latest values (distances in cm) polled from the sensor
        Returns:
            Function has no returns
    '''

    last20SecTimes=[]
    for i in range(1,22,3):
        last20SecTimes.append(i)

    plt.plot(last20SecTimes, polledData2)

    plt.xlabel('Timestamps (s)')
    plt.ylabel('Vehicle Height (cm)')
    plt.legend(['Vehicle Height'])
    plt.title("Polled vehicle heights from the last 20 seconds vs Time")
    plt.savefig('height_time_graph.png')
    plt.show()
    
def graphing_temperature(thermistorData):
    '''
    Function to create graph from sensor data
        Parameters:
            polledData (list of integers): list of latest values (distances in cm) polled from the sensor
        Returns:
            Function has no returns
    '''

    last20SecTimes=[]
    for i in range(1,22,3):
        last20SecTimes.append(i)

    plt.plot(last20SecTimes, thermistorData)

    plt.xlabel('Timestamps (s)')
    plt.ylabel('Temperature (°C)')
    plt.legend(['Temperature'])
    plt.title("Polled temperature mesurements from the last 20 seconds vs Time")
    plt.savefig('temp_time_graph.png')
    plt.show()
    
