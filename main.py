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


def read_func_old(filename):
    """ Outdated: Function to read data files and sort them into colors. \
    Returns a list of sample names, colors, and the data itself as matrix."""
    textfile = open(filename,"r")
    textfile.readline() #first two lines are not important
    textfile.readline()
    names = textfile.readline() #names are separated by multiple tabs
    names = names.split("\t")
    names[:] = [item for item in names if item != ''] #remove empty entries (between two \t's)
    colors = textfile.readline()
    colors = colors.split("\t")
    colors[:] = [item for item in colors if item != '']
    data = []           #fill with data
    for i in range(5000):
        line = textfile.readline()
        splitted = line.split("\t")
        splitted[:] = [int(item) for item in splitted if (item != '' and item != '\n')]
        data.append(splitted)
    data = np.array(data)
    return names,colors,data



def plot_func(titles, colors, data):
    counter = 0
    for i in range(len(titles)-1):
        for j in range(6):
            plt.figure()
            plt.plot(data[:,6*i+j], label=str(colors[6*i+j]))
        plt.legend()
        plt.title(titles[counter])
        plt.show()
        counter += 1
    return None


def plot_6C(title,colors,data):
    fig = plt.figure()
    for i in range(6):
        plt.subplot(3,2,i+1)
        plt.plot(data[:,i])
        plt.title(colors[i])
    plt.show()
    return fig


def plot_compare(data_raw,data_sized,titles,colors):
    #data_raw_short = data_raw[-len(data_sized)]
    difference = len(data_raw)-len(data_sized)
    data_raw_short = data_raw[difference::,:]
    counter = 0
    for i in range(len(titles)-1):
        for j in range(6):
            plt.figure()
            plt.plot(data_raw_short[:,6*i+j])
            plt.plot(data_sized[:, 6 * i + j])
            title = str(titles[i])+"_color_"+str(colors[6*i+j])
            plt.title(title)
            #plt.show()
            plt.savefig(str("raw_vs_sized"+title+".png"))
        counter += 1
    return None


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    sized_titles, sized_colors, sized_data = read_func('SizedTraceData.txt')
    raw_titles, raw_colors, raw_data = read_func('RawTraceData.txt')
    plot_compare(raw_data,sized_data,sized_titles,sized_colors)

