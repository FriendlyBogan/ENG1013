# Function to create graph from sensor data
# Created By : Team A12: Nudara, Cooper, Devni, Kristian, Naailah
# Created Date: 20/04/2024
# version: 5.0

import matplotlib.pyplot as plt

def graphing(polledData):
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
    plt.title("Polled data from the last 20 seconds")
    plt.show()
    plt.savefig('Polled data graph.pdf')
