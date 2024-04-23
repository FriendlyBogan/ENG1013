import matplotlib.pyplot as plt

def graphing(polledData):
    last20SecDistances = polledData[-1:-8:-1]
    last20SecTimes=[]
    for i in range(1,22,3):
        last20SecTimes.append(i)

    plt.plot(last20SecTimes, last20SecDistances)

    plt.xlabel('Timestamps')
    plt.ylabel('Distances (cm)')
    plt.show()
