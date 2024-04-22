import matplotlib as plt

def graphing(polledData):
    last20SecDistances = polledData[-1:-21]
    last20SecTimes=[]
    for i in range(1,21,1):
        last20SecTimes.append(i)

    plt.plot(last20SecDistances, last20SecTimes)

    plt.xlabel('Timestamps')
    plt.ylabel('Distances (cm)')
    plt.show()
