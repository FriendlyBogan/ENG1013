import matplotlib as plt

def graphing(polledData):
    last20SecDistances = polledData[-1:-81]
    last20SecTimes=[]
    for i in range(0.25,21,0.25):
        last20SecTimes.append(i)

    plt.plot(last20SecDistances, last20SecTimes)

    plt.xlabel('Timestamps')
    plt.ylabel('Distances (cm)')
    plt.show()
