import matplotlib.pyplot as plt
import numpy as np


# GLOBAL VARIABLES
# list of colors as they appear in (sized) data files
color_list = ['FL-6C', 'JOE-6C', 'TMR-6C', 'CXR-6C', 'TOM-6C', 'WEN-6C']
# dict of color names to colors to be plotted
color_dict = {'FL-6C': 'b', 'JOE-6C': 'g', 'TMR-6C': 'y', 'CXR-6C': 'r', 'WEN-6C': 'k', 'TOM-6C': 'm'}


def plot_data(data, titles):
    """"Plots all data per color for entire lists"""
    # take one off since last pocon is semi-empty?
    for i in range(len(titles)-1):
        plt.figure()
        for j in range(6):
            plt.plot(data[:, 6*i+j], label=str(color_list[j]))
        plt.legend()
        plt.title(titles[i])
        plt.show()
    return None


def plot_6C(data, titles):
    """"Plots one combined plot of all 6 colors of one hid file"""
    for j in range(len(titles)-1):
        fig = plt.figure()
        plt.suptitle(titles[j])
        for i in range(6):
            plt.subplot(6, 1, i + 1)
            plt.plot(data[:, 6 * j + i])
            plt.title(color_list[i % 6])
        plt.show()
    return None


def plot_raw_vs_sized(data_raw, data_sized, titles):
    """Currently broken, probably won't use anymore, so not fixin't"""
    difference = len(data_raw)-len(data_sized)
    data_raw_short = data_raw[difference::, :]
    counter = 0
    for i in range(len(titles)-1):
        for j in range(6):
            plt.figure()
            plt.plot(data_raw_short[:, 6 * i + j])
            plt.plot(data_sized[:, 6 * i + j])
            title = str(titles[i]) + "_color_" + str(color_list[j])
            plt.title(title)
            plt.show()
        counter += 1
    return None


def plot_compare(alleles, heights, allele_dict, dye_dict, comparison):
    """uses both the analysts identifies peak and sized data for comparison to plot both in one image"""
    for j in range(6):
        plt.figure()
        plt.title(str('filename: 1A2.3, color: ' + str(color_list[j])))
        plt.plot(np.linspace(0, 620, len(comparison[:, j])), comparison[:, j])
        for i in range(len(alleles)):
            # use dye_dict to plot correct color
            a, b = alleles[i].split("_")
            color = color_dict[dye_dict[a]]
            plt.plot([allele_dict[a][b]], [heights[i]], str(color + "*"))  # add colour
        plt.show()
    pass
