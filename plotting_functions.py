import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from GLOBALS import *

# list of colors in the order they appear in (sized) trace data files
color_list = ['FL-6C', 'JOE-6C', 'TMR-6C', 'CXR-6C', 'TOM-6C', 'WEN-6C']
# dict of color names to colors to be plotted
color_dict = {'FL-6C': 'b', 'JOE-6C': 'g', 'TMR-6C': 'y', 'CXR-6C': 'r', 'WEN-6C': 'k', 'TOM-6C': 'm'}


def plot_data(sample: Sample):
    """"Simple plot of all colors of one sample in the same figure"""
    plt.figure()
    for i in range(6):
        plt.plot(sample.data[:, i], label=str(color_list[i]))
    plt.legend()
    plt.title(sample.name)
    plt.show()
    return None


def plot_6C(sample: Sample):
    """"Plots one combined plot of all 6 colors of one hid file"""
    plt.figure()
    plt.suptitle(sample.name)
    for i in range(6):
        plt.subplot(6, 1, i + 1)
        plt.plot(sample.data[:, i])
        plt.title(color_list[i])
    plt.show()
    return None


def plot_compare(name: str, mixture: Mixture, locus_dict: dict, comparison: Sample):
    """uses both the analysts identified peaks and sized data \
    for comparison to plot both in one image"""
    for j in range(6):
        plt.figure()
        plt.title(str('filename: '+name+', dye: ' + str(color_list[j])))
        plt.xlim([50, 500])
        current_plot = comparison.data[:, j]
        plt.plot(np.linspace(0, len(current_plot)/10, len(current_plot)), comparison.data[:, j])
        plt.ylim([-50, max(current_plot[1000:])*1.5])
        for i in range(len(mixture.alleles)):
            # use dye_dict to plot correct color
            locus, allele = mixture.alleles[i].split("_")
            dye = locus_dict[locus].dye
            dye_name = dye.name
            color = dye.plot_color
            if dye_name == color_list[j]:
                plt.plot([locus_dict[locus].alleles[allele].mid], [mixture.heights[i]], str(color + "*"))  # add colour
        plt.show()
    pass


def plot_sizestd_peaks(sizestd):
    """The goal of this function was to determine the factor needed \
    for resizing the sized data to base pairs\
    Input is one size standard array, output was a plot"""
    peaks, rest = find_peaks(sizestd, distance=200)
    plt.figure()
    plt.plot(sizestd)
    print(peaks)
    plt.plot(peaks, sizestd[peaks], "*")
    plt.show()
    return None


def plot_actual(name: str, mix: Mixture, locus_dict: dict, comparison: Sample):
    """uses both the theoretical actual relative peaks and \
    sized data for comparison to plot both in one image"""

    for j in range(6):
        plt.figure()
        plt.title(str('filename: '+name+', dye: ' + str(color_list[j])))
        current_plot = comparison.data[:, j]
        plt.xlim([50, 500])
        plt.ylim([-50, max(current_plot[1000:]) * 1.5])
        max_rel = 20000
        plt.hlines(max_rel, 0, 500)
        plt.plot(np.linspace(0, len(current_plot)/10, len(current_plot)), comparison.data[:, j])
        for locus, value in locus_dict.items():
            for allele_name, allele in value.alleles.items():
                dye = value.dye
                if allele.height != 0 and dye.name == color_list[j]:
                    color = dye.plot_color
                    plt.plot([allele.mid], [allele.height*max_rel], str(color + "*"))  # add colour
        plt.show()
    pass


def plot_markers(locusDict):
    """Just a quick function to test marker boundaries"""
    plt.figure()
    for key_locus in locusDict:
        locus = locusDict[key_locus]
        plt.subplot(6, 1, locus.dye.plot_index)
        plt.plot([locus.lower, locus.upper], [0, 0], color = locus.dye.plot_color, marker = "s")
        for key_allele in locus.alleles:
            allele = locus.alleles[key_allele]
            start = allele.mid - allele.left
            end = allele.mid + allele.right
            plt.plot([start, end], [1,1])
    plt.show()
