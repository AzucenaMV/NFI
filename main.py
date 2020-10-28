import numpy as np
import matplotlib.pyplot as plt

def read_func(filename):
    """ Function to read data files and sort them into colors. \
    Returns a list of sample names, colors, and the data itself as matrix."""
    textfile = open(filename,"r")
    texts = textfile.read()
    texts = texts.split("\n")
    print(len(texts))
    for i in range(5):
        print(texts[i])
    # names = textfile.readline() #names are separated by multiple tabs
    # names = names.split("\t")
    # names[:] = [item for item in names if item != ''] #remove empty entries (between two \t's)
    # colors = textfile.readline()
    # colors = colors.split("\t")
    # colors[:] = [item for item in colors if item != '']
    # data = []           #fill with data
    # for i in range(5000):
    #     line = textfile.readline()
    #     splitted = line.split("\t")
    #     #splitted.remove("")
    #     splitted[:] = [int(item) for item in splitted if (item != '' and item != '\n')]
    #     data.append(splitted)
    # data = np.array(data)
    # #data = data.transpose()
    # return names,colors,data
    pass

def plot_func(names,colors,data):
    counter = 0
    for i in range(len(names)-1):
        fig = plt.figure()
        for j in range(6):
            plt.plot(data[:,6*i+j],label = str(colors[6*i+j]))
        plt.legend()
        plt.title(names[counter])
        plt.show()
        counter += 1
    pass


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    pass
    read_func('SizedTraceData.txt')
    #print(data.shape)
    #plot_func(names,colors,data)