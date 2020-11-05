import matplotlib.pyplot as plt
import numpy as np


def plot_data(data, titles, colors):
    """"Plots all single colors in lists"""
    counter = 0
    for i in range(len(titles)-1):
        for j in range(6):
            plt.figure()
            plt.plot(data[:, 6*i+j], label=str(colors[6*i+j]))
        plt.legend()
        plt.title(titles[counter])
        plt.show()
        counter += 1
    return None


def plot_6C(data, colors):
    """"Plots one 3x2 set of all 6 colors of one hid file"""
    fig = plt.figure()
    for i in range(6):
        plt.subplot(3, 2, i+1)
        plt.plot(data[:, i])
        plt.title(str(colors[i]))
    plt.show()
    return fig


def plot_raw_vs_sized(data_raw, data_sized, titles, colors):
    difference = len(data_raw)-len(data_sized)
    data_raw_short = data_raw[difference::, :]
    counter = 0
    for i in range(len(titles)-1):
        for j in range(6):
            plt.figure()
            plt.plot(data_raw_short[:, 6 * i + j])
            plt.plot(data_sized[:, 6 * i + j])
            title = str(titles[i]) + "_color_" + str(colors[6*i+j])
            plt.title(title)
            plt.show()
        counter += 1
    return None


def plot_actual(alleles, heights, allele_dict, dye_dict, comparison, colors):
    """uses both the analysts identifies peak and sized data for comparison to plot both in one image"""
    temp_dict = {'FL-6C': 'b', 'JOE-6C': 'g', 'TMR-6C': 'y', 'CXR-6C': 'r', 'WEN-6C': 'k', 'TOM-6C': 'm'}
    for j in range(6):
        plt.figure()
        plt.title(str('color is ' + str(colors[j])))
        plt.plot(np.linspace(0, 620, len(comparison[:, j])), comparison[:, j])
        for i in range(len(alleles)):
            # use dye_dict to plot correct color
            a, b = alleles[i].split("_")
            color = temp_dict[dye_dict[a]]
            plt.plot([allele_dict[a][b]], [heights[i]], str(color + "*"))  # add colour
        plt.show()
    pass
