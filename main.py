import numpy as np
import matplotlib.pyplot as plt


def read_func(filename):
    """ Function to read data files and sort them into colors. \
    Returns a list of sample names, colors, and the data itself as matrix."""
    textfile = open(filename, "r")
    texts = textfile.read()
    texts = texts.split("\n")
    # lines 1 and 2 are not interesting
    titles = texts[2].split('\t')                       # get titles of files
    titles = [item for item in titles if item != '']    # remove empty entries after splitting
    colors = texts[3].split('\t')                       # get names of colors
    data = np.zeros((len(texts[4:]),len(colors)))
    counter = 0
    for elt in texts[4:]:
        new = np.array(elt.split('\t'))
        new[new == ''] = 0
        data[counter,:] = new
        counter += 1
    return titles, colors, data


def plot_func(titles, colors, data):
    counter = 0
    for i in range(len(titles)-1):
        fig = plt.figure()
        for j in range(6):
            plt.plot(data[:][6*i+j], label=str(colors[6*i+j]))
        plt.legend()
        plt.title(titles[counter])
        plt.show()
        counter += 1
    return fig


def plot_6C(title,colors,data):
    fig = plt.figure()
    for i in range(6):
        plt.subplot(3,2,i+1)
        plt.plot(data[:,i])
        plt.title(colors[i])
    plt.show()
    return fig


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    pass
    sized_titles, sized_colors, sized_data = read_func('SizedTraceData.txt')
    plot_6C(sized_titles[0], sized_colors[0:6], sized_data[:,0:6])
    raw_titles, raw_colors, raw_data = read_func('RawTraceData.txt')
    plot_6C(raw_titles[0], raw_colors[0:6], raw_data[:,0:6])

